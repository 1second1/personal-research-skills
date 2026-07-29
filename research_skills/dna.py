"""Load and validate the repository's intentionally small YAML profile format."""

from __future__ import annotations

from pathlib import Path
import ast
import re


REQUIRED_SECTIONS = ("identity", "values", "thinking", "decision_rules", "workflows", "preferences")


def _scalar(value: str):
    value = value.strip()
    if not value:
        return {}
    if value.startswith(("'", '"')):
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value.strip("'\"")
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith("[") and value.endswith("]"):
        return [_scalar(part) for part in value[1:-1].split(",") if part.strip()]
    return value


def _strip_comment(line: str) -> str:
    if " #" in line:
        return line.split(" #", 1)[0].rstrip()
    return line.rstrip()


def _parse(text: str) -> dict:
    root: dict = {}
    stack: list[tuple[int, object]] = [(-1, root)]
    for line_number, raw in enumerate(text.splitlines(), 1):
        line = _strip_comment(raw)
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if "\t" in line[:indent]:
            raise ValueError(f"Tabs are not supported in profile line {line_number}")
        content = line.strip()
        while stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1]
        if content.startswith("- "):
            if not isinstance(parent, list):
                raise ValueError(f"List item has no list parent on line {line_number}")
            item_body = content[2:]
            if ":" in item_body:
                # List-of-objects: "- key: value" with optional nested children.
                item_key, item_value = item_body.split(":", 1)
                item_key = item_key.strip()
                if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]*", item_key):
                    raise ValueError(f"Invalid key {item_key!r} on line {line_number}")
                if item_value.strip():
                    child: object = {item_key: _scalar(item_value)}
                else:
                    next_content = ""
                    for future in text.splitlines()[line_number:]:
                        if future.strip() and not future.lstrip().startswith("#"):
                            next_content = future.strip()
                            break
                    child = {item_key: [] if next_content.startswith("-") else {}}
                parent.append(child)
                stack.append((indent, child))
            else:
                parent.append(_scalar(item_body))
            continue
        if ":" not in content:
            raise ValueError(f"Expected key/value on line {line_number}")
        key, raw_value = content.split(":", 1)
        key = key.strip()
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]*", key):
            raise ValueError(f"Invalid key {key!r} on line {line_number}")
        if not isinstance(parent, dict):
            raise ValueError(f"Mapping item has no mapping parent on line {line_number}")
        if raw_value.strip():
            parent[key] = _scalar(raw_value)
        else:
            next_content = ""
            for future in text.splitlines()[line_number:]:
                if future.strip() and not future.lstrip().startswith("#"):
                    next_content = future.strip()
                    break
            child: object = [] if next_content.startswith("-") else {}
            parent[key] = child
        stack.append((indent, parent[key]))
    return root


def load_profile(path: str | Path) -> dict:
    """Load a profile and reject missing or malformed top-level sections."""
    profile_path = Path(path)
    if not profile_path.is_file():
        raise FileNotFoundError(profile_path)
    profile = _parse(profile_path.read_text(encoding="utf-8"))
    missing = [section for section in REQUIRED_SECTIONS if section not in profile]
    if missing:
        raise ValueError("Profile missing required sections: " + ", ".join(missing))
    if not isinstance(profile["identity"], dict) or not profile["identity"].get("name"):
        raise ValueError("Profile identity.name is required")
    return profile


REQUIRED_CONTRACT_FIELDS = ("name", "version")


def load_contract(path: str | Path) -> dict:
    """Load a Skill contract and reject missing required fields."""
    contract_path = Path(path)
    if not contract_path.is_file():
        raise FileNotFoundError(contract_path)
    contract = _parse(contract_path.read_text(encoding="utf-8"))
    missing = [field for field in REQUIRED_CONTRACT_FIELDS if field not in contract]
    if missing:
        raise ValueError("Contract missing required fields: " + ", ".join(missing))
    return contract


def format_profile_rules(profile: dict) -> str:
    """Render the profile as deterministic instructions for a composed Skill."""
    lines = ["## Personal Reasoning DNA", "", f"Profile: {profile['identity']['name']}", ""]
    lines.append("### Values")
    lines.extend(f"- {item}" for item in profile["values"])
    lines.extend(["", "### Inquiry Pattern", f"{profile['thinking']['inquiry_pattern']}", ""])
    lines.append("### Thinking Rules")
    for key, value in profile["thinking"].items():
        if key != "inquiry_pattern":
            lines.append(f"- {key}: {value}")
    lines.extend(["", "### Decision Rules"])
    lines.extend(f"- {item}" for item in profile["decision_rules"])
    lines.extend(["", "### Output Preferences"])
    for key, value in profile["preferences"].items():
        lines.append(f"- {key}: {value}")
    return "\n".join(lines)
