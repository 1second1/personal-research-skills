"""Strict YAML loading and validation for methodology profiles and contracts."""
from pathlib import Path
import re
import yaml

class UniqueSafeLoader(yaml.SafeLoader):
    """Reject duplicate mapping keys while retaining safe YAML semantics."""
    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        result = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise ValueError("Mapping keys must be strings")
            if key in result:
                raise ValueError(f"Duplicate key: {key} at line {key_node.start_mark.line + 1}")
            result[key] = self.construct_object(value_node, deep=deep)
        return result

def _parse(text: str) -> dict:
    try:
        result = yaml.load(text, Loader=UniqueSafeLoader)
    except yaml.YAMLError as error:
        raise ValueError(f"Invalid YAML: {error}") from error
    if not isinstance(result, dict) or not result:
        raise ValueError("Expected a non-empty YAML mapping")
    return result

def _text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")

def _strings(value, field):
    if not isinstance(value, list) or not value:
        raise ValueError(f"{field} must be a non-empty list")
    for item in value:
        _text(item, field)

def _mapping(value, field):
    if not isinstance(value, dict) or not value:
        raise ValueError(f"{field} must be a non-empty mapping")
    for key, item in value.items():
        _text(item, f"{field}.{key}")

def _version(value, field):
    _text(value, field)
    if not re.fullmatch(r"\d+\.\d+\.\d+", value):
        raise ValueError(f"{field} must use major.minor.patch")

def load_profile(path: str | Path) -> dict:
    profile = _parse(Path(path).read_text(encoding="utf-8"))
    required = ("identity", "values", "thinking", "decision_rules", "workflows", "preferences")
    missing = [name for name in required if name not in profile]
    if missing:
        raise ValueError("Profile missing required sections: " + ", ".join(missing))
    for name in ("identity", "thinking", "workflows", "preferences"):
        _mapping(profile[name], name)
    _text(profile["identity"].get("name"), "identity.name")
    _version(profile["identity"].get("version"), "identity.version")
    _text(profile["thinking"].get("inquiry_pattern"), "thinking.inquiry_pattern")
    for name in ("values", "decision_rules"):
        _strings(profile[name], name)
    return profile

def load_contract(path: str | Path) -> dict:
    contract = _parse(Path(path).read_text(encoding="utf-8"))
    for name in ("name", "purpose"):
        _text(contract.get(name), name)
    _version(contract.get("version"), "version")
    for name in ("outputs", "constraints"):
        _strings(contract.get(name), name)
    if "evaluation" in contract:
        _strings(contract["evaluation"], "evaluation")
    inputs = contract.get("inputs")
    if not isinstance(inputs, list) or not inputs:
        raise ValueError("inputs must be a non-empty list")
    names = set()
    for item in inputs:
        if not isinstance(item, dict):
            raise ValueError("Each input must be a mapping")
        _text(item.get("name"), "inputs.name")
        _text(item.get("type"), "inputs.type")
        if not isinstance(item.get("required"), bool):
            raise ValueError("inputs.required must be boolean")
        if item["name"] in names:
            raise ValueError(f"Duplicate input: {item['name']}")
        names.add(item["name"])
    return contract

def format_profile_rules(profile: dict) -> str:
    lines = ["## Personal Reasoning DNA", "", f"Profile: {profile['identity']['name']}"]
    for heading, key in (
        ("Values", "values"), ("Thinking Rules", "thinking"),
        ("Decision Rules", "decision_rules"), ("Workflows", "workflows"),
        ("Output Preferences", "preferences"),
    ):
        lines.extend(["", f"### {heading}"])
        value = profile[key]
        if isinstance(value, dict):
            lines.extend(f"- {name}: {item}" for name, item in value.items())
        else:
            lines.extend(f"- {item}" for item in value)
    return "\n".join(lines)
