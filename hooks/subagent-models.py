#!/usr/bin/env python3
"""Only allow selected models for Task subagents.

Allowed today: composer-2.5, composer-2.5-fast, grok-4.7 at any thinking
level (grok-4.7, grok-4.7-high, and similar).
"""

from __future__ import annotations

import json
import sys

ALLOWED = frozenset({"composer-2.5", "composer-2.5-fast"})
DENY_MESSAGE = (
    "Subagent blocked: only composer-2.5, composer-2.5-fast, grok-4.7 "
    "(any thinking level) are allowed. Every subagent call must name one "
    "of these models explicitly."
)


def normalize_model(model: str | None) -> str:
    normalized = (model or "").strip().lower()
    return normalized.removeprefix("cursor-")


def allowed_subagent_model(model: str | None) -> bool:
    normalized = normalize_model(model)
    if not normalized:
        return False
    if normalized in ALLOWED:
        return True
    return normalized == "grok-4.7" or normalized.startswith("grok-4.7-")


def model_from_payload(payload: dict) -> str | None:
    for key in ("subagent_model", "model_id", "model"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return None


def task_model(payload: dict) -> str | None:
    tool_input = payload.get("tool_input")
    if isinstance(tool_input, dict):
        value = tool_input.get("model")
        if isinstance(value, str) and value.strip():
            return value
    return model_from_payload(payload)


def is_subagent_tool(payload: dict) -> bool:
    name = payload.get("tool_name")
    return isinstance(name, str) and name in {"Task", "Subagent"}


def decide(payload: dict) -> dict:
    event = str(payload.get("hook_event_name") or "")
    if event == "preToolUse":
        if not is_subagent_tool(payload):
            return {"permission": "allow"}
        model = task_model(payload)
        if allowed_subagent_model(model):
            return {"permission": "allow"}
        return {
            "permission": "deny",
            "user_message": DENY_MESSAGE,
            "agent_message": DENY_MESSAGE,
        }
    if allowed_subagent_model(model_from_payload(payload)):
        return {"permission": "allow"}
    return {"permission": "deny", "user_message": DENY_MESSAGE}


def main() -> None:
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        if not isinstance(payload, dict):
            raise ValueError("hook payload is not an object")
        json.dump(decide(payload), sys.stdout)
        sys.stdout.write("\n")
    except Exception:
        json.dump(
            {
                "permission": "deny",
                "user_message": DENY_MESSAGE,
                "agent_message": DENY_MESSAGE,
            },
            sys.stdout,
        )
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
