"""Verify frozen evaluation files, inventory, sizes and SHA-256 without changes.

This checks artifact integrity, not semantic quality or model authorization.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re


def _unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"Duplicate JSON key: {key}")
        value[key] = item
    return value


def verify_seal(manifest: Path, root: Path) -> list[str]:
    root = root.resolve()
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    except (OSError, ValueError) as error:
        return [f"Invalid seal: {error}"]
    if not isinstance(data, dict) or data.get("schema_version") != "1.0":
        return ["Invalid seal schema_version"]
    files, directories = data.get("files"), data.get("sealed_directories")
    if not isinstance(files, list) or not files or not isinstance(directories, list) or not directories:
        return ["Seal requires non-empty files and sealed_directories"]
    errors = []

    def contained(raw):
        if not isinstance(raw, str) or not raw.strip():
            errors.append("Invalid seal path")
            return None
        path = (root / raw).resolve()
        if Path(raw).is_absolute() or not path.is_relative_to(root):
            errors.append(f"Seal path escapes root: {raw}")
            return None
        return path

    scopes = []
    for raw in directories:
        directory = contained(raw)
        if directory is not None:
            if not directory.is_dir():
                errors.append(f"Missing sealed directory: {raw}")
            else:
                scopes.append(directory)
    listed = set()
    for entry in files:
        if not isinstance(entry, dict):
            errors.append("Invalid seal file entry")
            continue
        path = contained(entry.get("path"))
        if path is None:
            continue
        if path in listed:
            errors.append(f"Duplicate seal path: {entry['path']}")
        listed.add(path)
        if not any(path.is_relative_to(scope) for scope in scopes):
            errors.append(f"File outside sealed directories: {entry['path']}")
            continue
        digest, size = entry.get("sha256"), entry.get("size")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            errors.append(f"Invalid digest: {entry['path']}")
        if isinstance(size, bool) or not isinstance(size, int) or size < 0:
            errors.append(f"Invalid size: {entry['path']}")
        try:
            payload = path.read_bytes()
        except OSError as error:
            errors.append(f"Missing/unreadable sealed file: {entry['path']}: {error}")
            continue
        if len(payload) != size:
            errors.append(f"Size mismatch: {entry['path']}")
        if hashlib.sha256(payload).hexdigest() != digest:
            errors.append(f"Digest mismatch: {entry['path']}")
    for scope in scopes:
        for path in scope.rglob("*"):
            if path.is_file() and path.resolve() not in listed:
                errors.append(f"Unsealed file: {path.relative_to(root)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--root", type=Path)
    args = parser.parse_args()
    errors = verify_seal(args.manifest, args.root or args.manifest.parent)
    if errors:
        print("\n".join(errors))
        return 1
    print("Evaluation material seal verified (integrity only; model generation not authorized)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
