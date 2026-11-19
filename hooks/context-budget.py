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


def state_path(conversation_id: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", conversation_id)[:160]
    return STATE_DIR / f"{safe}.json"


def read_tokens(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        return int(json.loads(path.read_text()).get("tokens") or 0)
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return 0


def update_tokens(conversation_id: str, extra: int | None = None, replace: int | None = None) -> int:
    import fcntl

    if extra is not None and extra <= 0 and replace is None:
        return read_tokens(state_path(conversation_id))

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    path = state_path(conversation_id)
    lock_path = path.with_suffix(".lock")
    with lock_path.open("a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        total = replace if replace is not None else read_tokens(path) + (extra or 0)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"tokens": total}))
        os.replace(tmp, path)
        return total


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


def response_for(event: str, total: int, limit: int | None = None) -> dict:
    if event == "preToolUse":
        return {"permission": "allow"}
    if event == "beforeSubmitPrompt":
        return {"continue": True}
    notice = notice_for(total)
    if event == "postToolUse" and notice is not None:
        detail = f"{total} / {limit} tokens." if limit else f"{total} tokens."
        return {"additional_context": f"{notice}\n\nContext: {detail}"}
    return {}


def main() -> None:
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        if not isinstance(payload, dict):
            raise ValueError("hook payload is not an object")
        event = str(payload.get("hook_event_name") or "")
        conversation_id = str(payload.get("conversation_id") or "")
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
        json.dump(response_for(event, total, limit), sys.stdout)
        sys.stdout.write("\n")
    except Exception:
        json.dump(SAFE_FAILURE, sys.stdout)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
