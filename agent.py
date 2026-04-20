"""
Daily Reflection Tree — CLI Agent
Loads reflection-tree.json and walks the employee through the session.
No LLM calls at runtime. Fully deterministic.

Usage:
    python agent.py
    python agent.py --tree path/to/reflection-tree.json
"""

import json
import sys
import time
import textwrap
import argparse
from pathlib import Path


# ─── Helpers ────────────────────────────────────────────────────────────────

def slow_print(text: str, delay: float = 0.018, width: int = 72):
    """Print text character by character for a conversational feel."""
    wrapped = textwrap.fill(text, width=width)
    for char in wrapped:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def divider(char: str = "─", width: int = 72):
    print(char * width)


def blank():
    print()


def interpolate(text: str, state: dict) -> str:
    """Replace {axis1.dominant}, {axis2.dominant}, {axis3.dominant} placeholders."""
    text = text.replace("{axis1.dominant}", state["axis1"].get("dominant") or "—")
    text = text.replace("{axis2.dominant}", state["axis2"].get("dominant") or "—")
    text = text.replace("{axis3.dominant}", state["axis3"].get("dominant") or "—")
    for node_id, answer in state["answers"].items():
        text = text.replace(f"{{{node_id}.answer}}", answer)
    return text


# ─── State ──────────────────────────────────────────────────────────────────

def init_state() -> dict:
    return {
        "axis1": {"victor": 0, "victim": 0, "dominant": None},
        "axis2": {"contribution": 0, "entitlement": 0, "dominant": None},
        "axis3": {"altro": 0, "self": 0, "dominant": None},
        "answers": {},
        "summary_profile": None,
    }


def apply_signal(signal: str, state: dict):
    """Parse 'axis1:victor' and increment the right counter."""
    if not signal:
        return
    axis, pole = signal.split(":")
    state[axis][pole] += 1


def set_dominant(axis: str, state: dict):
    """Compute and store the dominant pole for an axis."""
    counts = {k: v for k, v in state[axis].items() if k not in ("dominant",)}
    dominant = max(counts, key=counts.get)
    state[axis]["dominant"] = dominant


# ─── Node Handlers ──────────────────────────────────────────────────────────

def handle_start(node: dict, state: dict) -> str:
    blank()
    divider("═")
    slow_print(node["text"])
    divider("═")
    blank()
    time.sleep(0.6)
    return node["next"]


def handle_question(node: dict, state: dict) -> str:
    blank()
    slow_print(node["text"])
    blank()

    options = node["options"]
    for opt in options:
        print(f"  {opt['label']})  {opt['text']}")
    blank()

    # Wait for valid input
    valid_labels = [opt["label"].upper() for opt in options]
    while True:
        raw = input("Your choice: ").strip().upper()
        if raw in valid_labels:
            break
        print(f"  Please enter one of: {', '.join(valid_labels)}")

    # Find the chosen option
    chosen = next(opt for opt in options if opt["label"].upper() == raw)

    # Store answer and apply signal
    state["answers"][node["id"]] = chosen["text"]
    apply_signal(chosen.get("signal", ""), state)

    blank()
    return chosen["next"]


def handle_decision(node: dict, state: dict) -> str:
    """Evaluate conditions in order; return next node for the first match."""
    for condition in node["conditions"]:
        if evaluate_condition(condition["if"], state):
            # Apply any set instruction
            apply_set(condition.get("set", ""), state)
            return condition["next"]
    # Fallback: use node-level next if defined
    return node.get("next", "END")


def evaluate_condition(condition_str: str, state: dict) -> bool:
    """
    Evaluate simple condition strings. Supported forms:
      - "true"
      - "state.axis1.victor >= state.axis1.victim"
      - "axis1.dominant == 'victor' AND axis2.dominant == 'contribution' AND axis3.dominant == 'altro'"
    """
    if condition_str.strip().lower() == "true":
        return True

    # Handle AND chains
    if " AND " in condition_str:
        parts = condition_str.split(" AND ")
        return all(evaluate_condition(p.strip(), state) for p in parts)

    # Normalize: strip leading "state."
    expr = condition_str.replace("state.", "")

    # axis1.victor >= axis1.victim  (numeric comparison)
    for op in [">=", ">", "<=", "<", "==", "!="]:
        if op in expr:
            left_str, right_str = expr.split(op, 1)
            left_val = resolve_value(left_str.strip(), state)
            right_val = resolve_value(right_str.strip(), state)
            return compare(left_val, right_val, op)

    return False


def resolve_value(token: str, state: dict):
    """Resolve a token like 'axis1.victor' or "'victor'" from state or as a literal."""
    token = token.strip()
    # String literal
    if token.startswith("'") and token.endswith("'"):
        return token[1:-1]
    # Dotted path into state
    parts = token.split(".")
    val = state
    for part in parts:
        if isinstance(val, dict):
            val = val.get(part)
        else:
            return None
    return val


def compare(left, right, op: str) -> bool:
    try:
        if op == ">=": return left >= right
        if op == ">":  return left > right
        if op == "<=": return left <= right
        if op == "<":  return left < right
        if op == "==": return left == right
        if op == "!=": return left != right
    except TypeError:
        return False
    return False


def apply_set(set_str: str, state: dict):
    """Apply a set instruction like "axis1.dominant = 'victor'" to state."""
    if not set_str:
        return
    left, right = set_str.split("=", 1)
    key_path = left.strip().split(".")
    value = resolve_value(right.strip(), state)
    target = state
    for part in key_path[:-1]:
        target = target[part]
    target[key_path[-1]] = value


def handle_reflection(node: dict, state: dict) -> str:
    blank()
    divider("·")
    slow_print(interpolate(node["text"], state), delay=0.022)
    divider("·")
    blank()
    input("  [ Press Enter to continue ] ")
    blank()
    return node["next"]


def handle_bridge(node: dict, state: dict) -> str:
    blank()
    slow_print(f"  ↳  {node['text']}", delay=0.015)
    blank()
    time.sleep(0.4)
    return node["next"]


def handle_summary(node: dict, state: dict) -> str:
    blank()
    divider("═")
    print("  YOUR REFLECTION SUMMARY")
    divider("═")
    blank()
    slow_print(interpolate(node["text"], state), delay=0.022)
    blank()
    divider("═")
    blank()
    input("  [ Press Enter to finish ] ")
    blank()
    return node["next"]


def handle_end(node: dict, state: dict) -> str:
    slow_print(node["text"])
    blank()
    return None  # Session complete


# ─── Dispatcher ─────────────────────────────────────────────────────────────

HANDLERS = {
    "start":      handle_start,
    "question":   handle_question,
    "decision":   handle_decision,
    "reflection": handle_reflection,
    "bridge":     handle_bridge,
    "summary":    handle_summary,
    "end":        handle_end,
}


# ─── Main Loop ──────────────────────────────────────────────────────────────

def load_tree(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Index nodes by id for O(1) lookup
    node_map = {node["id"]: node for node in data["nodes"]}
    return data, node_map


def run_session(tree_path: str):
    data, node_map = load_tree(tree_path)
    state = init_state()

    current_id = data["meta"]["entry"]  # "START"

    while current_id is not None:
        node = node_map.get(current_id)
        if node is None:
            print(f"[ERROR] Node '{current_id}' not found in tree.")
            break

        handler = HANDLERS.get(node["type"])
        if handler is None:
            print(f"[ERROR] Unknown node type '{node['type']}' at node '{current_id}'.")
            break

        current_id = handler(node, state)

    # Auto-compute dominants at end of session (in case decision nodes missed any)
    for axis in ("axis1", "axis2", "axis3"):
        if state[axis]["dominant"] is None:
            set_dominant(axis, state)


# ─── Entry Point ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Daily Reflection Tree — CLI Agent")
    parser.add_argument(
        "--tree",
        default="tree/reflection-tree.json",
        help="Path to the reflection tree JSON file (default: tree/reflection-tree.json)"
    )
    args = parser.parse_args()

    tree_path = Path(args.tree)
    if not tree_path.exists():
        print(f"Error: Tree file not found at '{tree_path}'")
        print("Usage: python agent.py --tree path/to/reflection-tree.json")
        sys.exit(1)

    try:
        run_session(str(tree_path))
    except KeyboardInterrupt:
        print("\n\n  Session ended early. See you tomorrow.")
        sys.exit(0)


if __name__ == "__main__":
    main()
