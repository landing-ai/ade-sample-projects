"""Flatten a JSON Schema into the ordered list of leaf fields the reviewer edits.

Walking the schema rather than the extraction matters for two reasons: panel
order follows schema order, and fields ADE returned nothing for still appear.
Array lengths are the exception, since they are data-dependent -- those are
enumerated from the extracted values.

Paths are dotted with bracketed array indices: `shipper.name`,
`containers[0].container_number`, `goods.itemized_list[2].gross_weight`.
"""

from __future__ import annotations

import re
from typing import Any

_INDEX_RE = re.compile(r"\[(\d+)\]")
_TOKEN_RE = re.compile(r"([^.\[\]]+)|\[(\d+)\]")


def parse_path(path: str) -> list[str | int]:
    """`containers[0].container_number` -> ['containers', 0, 'container_number']"""
    parts: list[str | int] = []
    for m in _TOKEN_RE.finditer(path):
        name, index = m.group(1), m.group(2)
        parts.append(name if name is not None else int(index))
    return parts


def get_by_path(data: Any, path: str) -> Any:
    node = data
    for key in parse_path(path):
        if isinstance(key, int):
            if not isinstance(node, list) or key >= len(node):
                return None
            node = node[key]
        else:
            if not isinstance(node, dict) or key not in node:
                return None
            node = node[key]
    return node


def set_by_path(data: dict, path: str, value: Any) -> None:
    """Set a value in-place, creating intermediate dicts/lists as needed."""
    keys = parse_path(path)
    node: Any = data
    for i, key in enumerate(keys[:-1]):
        nxt = keys[i + 1]
        if isinstance(key, int):
            while len(node) <= key:
                node.append([] if isinstance(nxt, int) else {})
            if node[key] is None:
                node[key] = [] if isinstance(nxt, int) else {}
            node = node[key]
        else:
            if key not in node or node[key] is None:
                node[key] = [] if isinstance(nxt, int) else {}
            node = node[key]
    last = keys[-1]
    if isinstance(last, int):
        while len(node) <= last:
            node.append(None)
        node[last] = value
    else:
        node[last] = value


def humanize(segment: str) -> str:
    base = _INDEX_RE.sub("", segment)
    text = base.replace("_", " ").strip()
    return text[:1].upper() + text[1:] if text else segment


def flatten_schema(schema: dict, extraction: dict | None) -> list[dict]:
    """Ordered leaf fields for the review panel.

    Each row: {path, label, description, type, ade_value}.
    """
    extraction = extraction or {}
    rows: list[dict] = []

    def walk(node: dict, path: str, label_segment: str) -> None:
        if not isinstance(node, dict):
            return
        node_type = node.get("type")

        if node_type == "object" or "properties" in node:
            props = node.get("properties") or {}
            for key, child in props.items():
                child_path = f"{path}.{key}" if path else key
                walk(child, child_path, key)
            return

        if node_type == "array":
            items = node.get("items") or {}
            values = get_by_path(extraction, path) if path else None
            count = len(values) if isinstance(values, list) else 0
            for i in range(count):
                walk(items, f"{path}[{i}]", f"{label_segment}[{i}]")
            return

        # Scalar leaf.
        rows.append(
            {
                "path": path,
                "label": humanize(label_segment),
                "description": node.get("description") or "",
                "type": node_type or "string",
                "ade_value": get_by_path(extraction, path),
            }
        )

    walk(schema, "", "")
    return rows
