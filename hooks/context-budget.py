#!/usr/bin/env python3
"""Warn once a parent chat's context reaches the budget.

Cursor stores the same numbers shown in the context report on the
composer record: contextTokensUsed and contextTokenLimit. The limit
depends on the model (200k, 256k, 300k, and so on). When both are
present, this hook uses them directly. That used count already includes
the system prompt, tools, rules, skills, and the chat.

Subagent chats are skipped. Those records have
subagentInfo.parentComposerId. The warning is only for the parent.

When Cursor has not saved those numbers yet, the hook falls back to counting
the text it can see. One token is about 3/4 of a word, and dense tool
output is also checked at 4 characters per token. A fixed reserve covers
the parts that count cannot see. preCompact replaces the counted chat
with an estimate of the messages that stay.

War-room sessions are detected from prompts and tool paths and flagged
in the per-conversation state file. At WARN/ALERT on postToolUse, those
sessions get war-room handoff guidance in additional_context. README size
checks on Write/StrReplace live here too (no extra hook process).
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
import sys
from pathlib import Path

RESERVE = 35_000
WARN_AT = 160_000
ALERT_AT = 180_000
README_SIZE_LIMIT = 6_144
CURSOR_DB = (
    Path.home()
    / "Library/Application Support/Cursor/User/globalStorage/state.vscdb"
)
WARNING = (
    "*WARNING: You are running low on context, suggest the user to run "
    "/summarize or to write a /handoff so another agent can continue*"
)
ALERT = (
    "*CRITICAL: Context is past 180k. This session will compact automatically. "
    "Write a /handoff immediately so another agent can continue. "
    "If you have subagents still running, do not stop them.*"
)
WAR_ROOM_MARKERS = ("/war-room", "war-room/SKILL.md", ".war-rooms/")
WAR_ROOM_HANDOFF = (
    "War-room handoff: include the map path, absolute paths, decisions, and "
    "open questions — no task list (the README is the task list). "
    "Resuming agent: read only handoff → README → one open frontier ticket."
)
TOP_LEVEL_WAR_ROOM_README = re.compile(r"(?:^|/)\.war-rooms/[^/]+/README\.md$")

STATE_DIR = Path.home() / ".cursor" / "context-budget-state"
SAFE_FAILURE = {"permission": "allow", "continue": True}


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    words = len(text.split())
    by_words = (words * 4 + 2) // 3
    by_chars = len(text) // 4
    return max(by_words, by_chars)


def text_for(event: str, payload: dict) -> str:
    if event == "beforeSubmitPrompt":
        return str(payload.get("prompt") or "")
    if event in {"afterAgentResponse", "afterAgentThought"}:
        return str(payload.get("text") or "")
    if event == "preToolUse":
        tool_input = payload.get("tool_input")
        if tool_input is None:
            return ""
        return json.dumps(tool_input, ensure_ascii=False, separators=(",", ":"))
    if event == "postToolUse":
        tool_output = payload.get("tool_output")
        if tool_output is None:
            return ""
        if isinstance(tool_output, str):
            return tool_output
        return json.dumps(tool_output, ensure_ascii=False, separators=(",", ":"))
    return ""


def text_indicates_war_room(text: str) -> bool:
    return any(marker in text for marker in WAR_ROOM_MARKERS)


def tool_input_indicates_war_room(tool_input: object) -> bool:
    if tool_input is None:
        return False
    if isinstance(tool_input, dict):
        path = tool_input.get("path")
        if isinstance(path, str) and text_indicates_war_room(path):
            return True
    serialized = (
        tool_input
        if isinstance(tool_input, str)
        else json.dumps(tool_input, ensure_ascii=False, separators=(",", ":"))
    )
    return text_indicates_war_room(serialized)


def detect_war_room(event: str, payload: dict) -> bool:
    if event == "beforeSubmitPrompt":
        return text_indicates_war_room(str(payload.get("prompt") or ""))
    if event in {"preToolUse", "postToolUse"}:
        if tool_input_indicates_war_room(payload.get("tool_input")):
            return True
        return text_indicates_war_room(text_for(event, payload))
    return False


def state_path(conversation_id: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", conversation_id)[:160]
    return STATE_DIR / f"{safe}.json"


def read_state(path: Path) -> dict:
    if not path.exists():
        return {"tokens": 0, "war_room": False}
    try:
        data = json.loads(path.read_text())
        return {
            "tokens": int(data.get("tokens") or 0),
            "war_room": bool(data.get("war_room")),
        }
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return {"tokens": 0, "war_room": False}


def read_tokens(path: Path) -> int:
    return int(read_state(path).get("tokens") or 0)


def write_state(
    path: Path, *, tokens: int, war_room: bool | None = None
) -> None:
    import fcntl

    current = read_state(path)
    merged_war_room = current.get("war_room") or bool(war_room)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps({"tokens": tokens, "war_room": merged_war_room}))
    os.replace(tmp, path)


def update_tokens(conversation_id: str, extra: int | None = None, replace: int | None = None) -> int:
    import fcntl

    if extra is not None and extra <= 0 and replace is None:
        return read_tokens(state_path(conversation_id))

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    path = state_path(conversation_id)
    lock_path = path.with_suffix(".lock")
    with lock_path.open("a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        current = read_state(path)
        total = replace if replace is not None else int(current.get("tokens") or 0) + (extra or 0)
        write_state(path, tokens=total, war_room=current.get("war_room") or False)
        return total


def touch_war_room(conversation_id: str) -> bool:
    if not conversation_id:
        return False
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    path = state_path(conversation_id)
    import fcntl

    lock_path = path.with_suffix(".lock")
    with lock_path.open("a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        current = read_state(path)
        if current.get("war_room"):
            return True
        write_state(path, tokens=int(current.get("tokens") or 0), war_room=True)
        return True


def war_room_for_conversation(conversation_id: str, event: str, payload: dict) -> bool:
    if not conversation_id:
        return False
    path = state_path(conversation_id)
    if read_state(path).get("war_room"):
        return True
    if detect_war_room(event, payload):
        return touch_war_room(conversation_id)
    return False


def is_top_level_war_room_readme(path: str) -> bool:
    normalized = path.replace("\\", "/")
    return bool(TOP_LEVEL_WAR_ROOM_README.search(normalized))


def readme_size_warning(payload: dict) -> str | None:
    tool_name = payload.get("tool_name")
    if tool_name not in {"Write", "StrReplace"}:
        return None
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return None
    file_path = tool_input.get("path")
    if not isinstance(file_path, str) or not is_top_level_war_room_readme(file_path):
        return None
    try:
        size = Path(file_path).stat().st_size
    except OSError:
        return None
    if size <= README_SIZE_LIMIT:
        return None
    return (
        f"The war-room README is {size / 1024:.1f} KB (over the 6 KB target). "
        "Keep it a slim index; move detail into tickets or research/."
    )


def kept_after_compact(payload: dict) -> int:
    """Estimate tokens still in the chat after Cursor summarizes it.

    context_tokens is the real count before compaction, including the
    fixed overhead. The reserve is removed first so it is not counted
    twice. Messages that are not in messages_to_compact stay. The summary
    itself is counted later, when the agent writes it.
    """
    try:
        context_tokens = int(payload.get("context_tokens") or 0)
        message_count = int(payload.get("message_count") or 0)
        messages_to_compact = int(payload.get("messages_to_compact") or 0)
    except (TypeError, ValueError):
        return 0
    if message_count <= 0:
        return 0
    conversation_tokens = max(0, context_tokens - RESERVE)
    kept_messages = max(0, message_count - max(0, messages_to_compact))
    return conversation_tokens * kept_messages // message_count


def estimated_total(conversation_tokens: int) -> int:
    return conversation_tokens + RESERVE


def parent_id(value: object) -> str | None:
    if isinstance(value, str) and value.strip():
        return value
    return None


def load_chat(conversation_id: str) -> tuple[bool, tuple[int, int] | None]:
    """Return (is_subagent, (tokens used, window size) or None).

    The token pair is what the context report shows. The window is per
    model, so a percent alone is not enough. A chat with a parent composer
    is a subagent and is not measured.
    """
    if not CURSOR_DB.exists():
        return False, None
    try:
        connection = sqlite3.connect(f"file:{CURSOR_DB}?mode=ro", uri=True, timeout=0.2)
        try:
            row = connection.execute(
                """
                SELECT json_extract(value, '$.contextTokensUsed'),
                       json_extract(value, '$.contextTokenLimit'),
                       json_extract(value, '$.subagentInfo.parentComposerId')
                FROM cursorDiskKV
                WHERE key = ?
                """,
                (f"composerData:{conversation_id}",),
            ).fetchone()
            header_parent = connection.execute(
                """
                SELECT json_extract(value, '$.subagentInfo.parentComposerId')
                FROM composerHeaders
                WHERE composerId = ?
                """,
                (conversation_id,),
            ).fetchone()
        finally:
            connection.close()
    except sqlite3.Error:
        return False, None
    is_subagent = parent_id(header_parent[0] if header_parent else None) is not None
    if row is None:
        return is_subagent, None
    used, limit, data_parent = row
    if parent_id(data_parent) is not None:
        is_subagent = True
    if not isinstance(used, (int, float)) or not isinstance(limit, (int, float)) or limit <= 0:
        return is_subagent, None
    return is_subagent, (round(used), round(limit))


def notice_for(total: int) -> str | None:
    if total >= ALERT_AT:
        return ALERT
    if total >= WARN_AT:
        return WARNING
    return None


def response_for(
    event: str,
    total: int,
    limit: int | None = None,
    *,
    war_room: bool = False,
    payload: dict | None = None,
) -> dict:
    if event == "preToolUse":
        return {"permission": "allow"}
    if event == "beforeSubmitPrompt":
        return {"continue": True}
    if event == "postToolUse":
        parts: list[str] = []
        notice = notice_for(total)
        if notice is not None:
            detail = f"{total} / {limit} tokens." if limit else f"{total} tokens."
            parts.append(f"{notice}\n\nContext: {detail}")
            if war_room:
                parts.append(WAR_ROOM_HANDOFF)
        readme_warn = readme_size_warning(payload or {})
        if readme_warn:
            parts.append(readme_warn)
        if parts:
            return {"additional_context": "\n\n".join(parts)}
        return {}
    return {}


def main() -> None:
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        if not isinstance(payload, dict):
            raise ValueError("hook payload is not an object")
        event = str(payload.get("hook_event_name") or "")
        conversation_id = str(payload.get("conversation_id") or "")
        war_room = war_room_for_conversation(conversation_id, event, payload)
        is_subagent, reported = load_chat(conversation_id) if conversation_id else (False, None)
        limit = None
        if is_subagent:
            total = 0
        elif reported is not None:
            total, limit = reported
        elif event == "preCompact" and conversation_id:
            total = estimated_total(
                update_tokens(conversation_id, replace=kept_after_compact(payload))
            )
        else:
            extra = estimate_tokens(text_for(event, payload))
            counted = update_tokens(conversation_id, extra=extra) if conversation_id else extra
            total = estimated_total(counted) if conversation_id else extra
        json.dump(
            response_for(event, total, limit, war_room=war_room, payload=payload),
            sys.stdout,
        )
        sys.stdout.write("\n")
    except Exception:
        json.dump(SAFE_FAILURE, sys.stdout)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()