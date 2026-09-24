#!/usr/bin/env python3
"""Validate a marketing-pack handoff and scaffold a visual production return.

JSON works with the Python standard library. YAML input uses PyYAML when it is
available. The emitted `.yaml` files contain JSON, which is valid YAML 1.2.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import struct
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from render_html_template import TEMPLATE_FILES, canvas_size, fill_template, try_png_export


ROOT = Path(__file__).resolve().parents[1]
SKILL_VERSION = "0.4.2"
ALLOWED_MODES = {"image-kit", "video-kit", "both", "qa-only"}
REMOTE_PREFIXES = ("http://", "https://", "data:", "file:")
FEATURE_POSTER_IDS = {"tpl-feature-poster", "tpl-feature-poster-zh"}


def load_document(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json" or text.lstrip().startswith("{"):
        data = json.loads(text)
    else:
        try:
            import yaml  # type: ignore
        except ImportError:
            data = parse_yaml_subset(text)
        else:
            data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise SystemExit("Handoff root must be a mapping/object.")
    return data


def strip_yaml_comment(line: str) -> str:
    quote = ""
    for i, char in enumerate(line):
        if char in {"'", '"'}:
            if not quote:
                quote = char
            elif quote == char:
                quote = ""
        elif char == "#" and not quote and (i == 0 or line[i - 1].isspace()):
            return line[:i].rstrip()
    return line.rstrip()


def yaml_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    lower = value.lower()
    if lower in {"true", "false"}:
        return lower == "true"
    if lower in {"null", "~"}:
        return None
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [yaml_scalar(part.strip()) for part in inner.split(",")]
    try:
        return float(value) if "." in value else int(value)
    except ValueError:
        return value


def parse_yaml_subset(text: str) -> Any:
    """Parse the mappings/lists/scalars used by the packaged handoff examples."""
    lines: list[tuple[int, str]] = []
    for raw in text.splitlines():
        clean = strip_yaml_comment(raw)
        if not clean.strip():
            continue
        indent = len(clean) - len(clean.lstrip(" "))
        lines.append((indent, clean.strip()))
    index = 0

    def parse_block(indent: int) -> Any:
        nonlocal index
        if index >= len(lines):
            return {}
        is_list = lines[index][1].startswith("- ") or lines[index][1] == "-"
        if is_list:
            result_list: list[Any] = []
            while index < len(lines):
                current_indent, content = lines[index]
                if current_indent != indent or not (content.startswith("- ") or content == "-"):
                    break
                rest = content[1:].strip()
                index += 1
                if not rest:
                    if index < len(lines) and lines[index][0] > indent:
                        result_list.append(parse_block(lines[index][0]))
                    else:
                        result_list.append(None)
                    continue
                if ":" not in rest:
                    result_list.append(yaml_scalar(rest))
                    continue
                key, value = rest.split(":", 1)
                item: dict[str, Any] = {}
                value = value.strip()
                if value:
                    item[key.strip()] = yaml_scalar(value)
                elif index < len(lines) and lines[index][0] > indent:
                    item[key.strip()] = parse_block(lines[index][0])
                else:
                    item[key.strip()] = {}
                if index < len(lines) and lines[index][0] > indent:
                    continuation = parse_block(lines[index][0])
                    if isinstance(continuation, dict):
                        item.update(continuation)
                result_list.append(item)
            return result_list

        result_map: dict[str, Any] = {}
        while index < len(lines):
            current_indent, content = lines[index]
            if current_indent != indent or content.startswith("-"):
                break
            if ":" not in content:
                raise SystemExit(f"Unsupported YAML line: {content}")
            key, value = content.split(":", 1)
            key = key.strip()
            value = value.strip()
            index += 1
            if value:
                result_map[key] = yaml_scalar(value)
            elif index < len(lines) and lines[index][0] > indent:
                result_map[key] = parse_block(lines[index][0])
            else:
                result_map[key] = {}
        return result_map

    return parse_block(lines[0][0]) if lines else {}


def dump_yaml_compatible(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def index_by_id(items: Any, label: str, errors: list[str]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    if items is None:
        return result
    if not isinstance(items, list):
        errors.append(f"{label} must be a list")
        return result
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"{label}[{i}] must be an object")
            continue
        key = str(item.get("id") or "").strip()
        if not key:
            errors.append(f"{label}[{i}] is missing id")
        elif key in result:
            errors.append(f"{label} contains duplicate id {key!r}")
        else:
            result[key] = item
    return result


def expected_dimensions(template_id: str) -> str:
    width, height = canvas_size(template_id)
    return f"{width}x{height}"


def normalize_dimensions(value: Any) -> str:
    return re.sub(r"\s+", "", str(value or "")).lower().replace("×", "x")


def resolve_source_path(raw: str, handoff_dir: Path) -> str:
    if raw.startswith(REMOTE_PREFIXES):
        return raw
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = handoff_dir / path
    return str(path.resolve())


def bind_payload(
    deliverable: dict[str, Any],
    base_payload: dict[str, Any],
    copy_index: dict[str, dict[str, Any]],
    source_index: dict[str, dict[str, Any]],
    handoff_dir: Path,
) -> tuple[dict[str, Any], list[str], list[str]]:
    payload = copy.deepcopy(base_payload)
    payload["locale"] = deliverable.get("locale") or payload.get("locale") or "en"
    payload["text"] = dict(payload.get("text") or {})
    payload["images"] = dict(payload.get("images") or {})
    blockers: list[str] = []
    used_sources: list[str] = []

    bindings = deliverable.get("slot_bindings") or {}
    text_bindings = dict(bindings.get("text") or {}) if isinstance(bindings, dict) else {}
    image_bindings = dict(bindings.get("images") or {}) if isinstance(bindings, dict) else {}

    if not text_bindings and deliverable.get("primary_copy_id"):
        text_bindings["headline"] = deliverable["primary_copy_id"]
    if "subcopy" not in text_bindings and deliverable.get("supporting_copy_ids"):
        text_bindings["subcopy"] = deliverable["supporting_copy_ids"][0]
    if not image_bindings:
        if deliverable.get("logo_asset_ids"):
            image_bindings["logo"] = deliverable["logo_asset_ids"][0]
        if deliverable.get("product_ui_asset_ids"):
            image_bindings["ui-screenshot"] = deliverable["product_ui_asset_ids"][0]

    for slot, copy_id in text_bindings.items():
        record = copy_index.get(str(copy_id))
        if not record or record.get("text") in (None, ""):
            blockers.append(f"text slot {slot!r} references missing approved copy {copy_id!r}")
            continue
        payload["text"][str(slot)] = str(record["text"])

    for slot, source_id in image_bindings.items():
        record = source_index.get(str(source_id))
        if not record:
            blockers.append(f"image slot {slot!r} references missing source asset {source_id!r}")
            continue
        rights = str(record.get("rights") or record.get("rights_status") or "").strip()
        raw_path = str(record.get("path") or record.get("url") or "").strip()
        if not rights:
            blockers.append(f"source asset {source_id!r} has no rights status")
        if not raw_path:
            blockers.append(f"source asset {source_id!r} has no path or URL")
            continue
        resolved = resolve_source_path(raw_path, handoff_dir)
        if not resolved.startswith(REMOTE_PREFIXES) and not Path(resolved).is_file():
            blockers.append(f"source asset {source_id!r} does not exist at {resolved}")
            continue
        payload["images"][str(slot)] = {
            "src": resolved,
            "alt": str(record.get("alt") or deliverable.get("alt_text") or slot),
        }
        used_sources.append(str(source_id))

    return payload, blockers, used_sources


def png_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        with path.open("rb") as handle:
            header = handle.read(24)
        if header[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        return struct.unpack(">II", header[16:24])
    except OSError:
        return None


def file_record(path: Path) -> dict[str, Any]:
    return {
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def asset_filename(asset_id: str, template_id: str, locale: str) -> str:
    return f"{asset_id}__{expected_dimensions(template_id)}__{locale}.png"


def render_deliverable(
    deliverable: dict[str, Any],
    base_payload: dict[str, Any],
    copy_index: dict[str, dict[str, Any]],
    source_index: dict[str, dict[str, Any]],
    handoff_dir: Path,
    run_dir: Path,
    request_png: bool,
) -> tuple[dict[str, Any], list[str]]:
    asset_id = str(deliverable.get("asset_id") or deliverable.get("frame_id") or "").strip()
    template_id = str(deliverable.get("template_id") or "").strip()
    locale = str(deliverable.get("locale") or base_payload.get("locale") or "en")
    blockers: list[str] = []

    if not asset_id:
        asset_id = "missing-asset-id"
        blockers.append("deliverable is missing asset_id/frame_id")
    if template_id not in TEMPLATE_FILES:
        blockers.append(f"unknown template_id {template_id!r}")
    else:
        template_text = (ROOT / "assets" / "templates" / "html" / TEMPLATE_FILES[template_id]).read_text(
            encoding="utf-8"
        )
        available_slots = set(re.findall(r'data-slot="([^"]+)"', template_text))
        bindings = deliverable.get("slot_bindings") or {}
        if isinstance(bindings, dict):
            for family in ("text", "images"):
                family_bindings = bindings.get(family) or {}
                if isinstance(family_bindings, dict):
                    for slot in family_bindings:
                        if str(slot) not in available_slots:
                            blockers.append(
                                f"{family} slot {slot!r} does not exist in template {template_id}"
                            )
        supplied_dims = normalize_dimensions(deliverable.get("dimensions") or deliverable.get("resolution"))
        expected = expected_dimensions(template_id)
        if supplied_dims and supplied_dims != expected:
            blockers.append(f"dimensions {supplied_dims!r} do not match {template_id} ({expected})")

    payload, binding_blockers, sources = bind_payload(
        deliverable, base_payload, copy_index, source_index, handoff_dir
    )
    blockers.extend(binding_blockers)

    if template_id in FEATURE_POSTER_IDS:
        text_payload = payload.get("text") if isinstance(payload.get("text"), dict) else {}
        image_payload = payload.get("images") if isinstance(payload.get("images"), dict) else {}
        if not str(text_payload.get("url") or "").strip():
            blockers.append(
                "feature poster requires a non-empty url text slot for the lower-right footer"
            )
        if not (image_payload.get("ui-screenshot") or image_payload.get("hero")):
            blockers.append(
                "feature poster requires a supplied ui-screenshot or hero source for its replaceable middle slot"
            )

    record: dict[str, Any] = {
        "asset_id": asset_id,
        "template_id": template_id,
        "filename": "",
        "path": "",
        "mime_type": "",
        "bytes": None,
        "sha256": "",
        "dimensions_or_duration": expected_dimensions(template_id) if template_id in TEMPLATE_FILES else "",
        "locale": locale,
        "copy_ids": list((deliverable.get("slot_bindings") or {}).get("text", {}).values()),
        "source_asset_ids": sources,
        "production_method": "pack-handoff bridge + packaged HTML template",
        "editable_source_path": "",
        "deviations": [],
        "full_quality_verified": False,
        "qa": {"result": "pending", "checked_at": "", "notes": "Visual and brand QA still required."},
        "status": "blocked" if blockers else "in-production",
    }

    if template_id not in TEMPLATE_FILES:
        return record, blockers

    payload_path = run_dir / "production" / "payloads" / f"{asset_id}.json"
    dump_yaml_compatible(payload_path, payload)
    editable_dir = run_dir / "editable" / asset_id
    html_path = fill_template(template_id, payload, editable_dir)
    record["editable_source_path"] = str(html_path.relative_to(run_dir))

    if request_png and not blockers:
        media_path = run_dir / "media" / asset_filename(asset_id, template_id, locale)
        media_path.parent.mkdir(parents=True, exist_ok=True)
        width, height = canvas_size(template_id)
        ok, message = try_png_export(html_path, media_path, width, height)
        if ok:
            dims = png_dimensions(media_path)
            if dims != (width, height):
                blockers.append(f"PNG dimensions are {dims}, expected {(width, height)}")
                record["status"] = "blocked"
            else:
                record.update(file_record(media_path))
                record["filename"] = media_path.name
                record["path"] = str(media_path.relative_to(run_dir))
                record["mime_type"] = "image/png"
                record["qa"]["notes"] = "File identity and dimensions pass; visual/brand QA pending."
        else:
            blockers.append(message)
            record["status"] = "blocked"

    return record, blockers


def write_video_docs(run_dir: Path, videos: list[dict[str, Any]]) -> list[dict[str, str]]:
    if not videos:
        return []
    storyboard = ["# Storyboard", "", "Storyboard frames are production inputs, not final video.", ""]
    shots: list[dict[str, Any]] = []
    for video in videos:
        storyboard.extend([f"## {video.get('asset_id', 'video')}", ""])
        for frame in video.get("frames") or []:
            storyboard.extend(
                [
                    f"### {frame.get('frame_id', 'frame')}",
                    "",
                    f"- Timecode: {frame.get('timecode', '')}",
                    f"- Template: {frame.get('template_id', '')}",
                    f"- Communication job: {frame.get('communication_job', '')}",
                    "",
                ]
            )
        for shot in video.get("shots") or []:
            if isinstance(shot, dict):
                shots.append({"video_asset_id": video.get("asset_id", ""), **shot})
    docs_dir = run_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "storyboard.md").write_text("\n".join(storyboard), encoding="utf-8")
    dump_yaml_compatible(docs_dir / "shot-list.yaml", {"schema_version": 1, "shots": shots})
    return [
        {"path": "docs/storyboard.md", "kind": "storyboard"},
        {"path": "docs/shot-list.yaml", "kind": "shot-list"},
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a visual-production run from a marketing-pack handoff.")
    parser.add_argument("--handoff", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True, help="Parent output directory")
    parser.add_argument("--png", action="store_true", help="Attempt batch PNG export with Playwright/Chromium")
    parser.add_argument("--check-only", action="store_true", help="Validate only; do not write a return package")
    args = parser.parse_args()

    handoff_path = args.handoff.resolve()
    handoff = load_document(handoff_path)
    errors: list[str] = []
    mode = str(handoff.get("mode") or "").strip()
    handoff_id = str(handoff.get("handoff_id") or "").strip()
    for field in ("handoff_id", "brief_version", "brand", "approval_owner"):
        if not str(handoff.get(field) or "").strip():
            errors.append(f"handoff is missing {field}")
    if mode not in ALLOWED_MODES:
        errors.append(f"mode must be one of {sorted(ALLOWED_MODES)}, got {mode!r}")

    copy_index = index_by_id(handoff.get("approved_copy"), "approved_copy", errors)
    source_index = index_by_id(handoff.get("source_assets"), "source_assets", errors)
    images = handoff.get("image_deliverables") or []
    videos = handoff.get("video_deliverables") or []
    if not isinstance(images, list):
        errors.append("image_deliverables must be a list")
        images = []
    if not isinstance(videos, list):
        errors.append("video_deliverables must be a list")
        videos = []
    if mode in {"image-kit", "both"} and not images:
        errors.append(f"mode {mode!r} requires image_deliverables")
    if mode in {"video-kit", "both"} and not videos:
        errors.append(f"mode {mode!r} requires video_deliverables")

    base_payload = handoff.get("brand_payload") or {}
    if not isinstance(base_payload, dict):
        errors.append("brand_payload must be an object")
        base_payload = {}

    if errors or args.check_only:
        print(json.dumps({"handoff_id": handoff_id, "valid": not errors, "errors": errors}, ensure_ascii=False, indent=2))
        return 1 if errors else 0

    run_dir = args.out.resolve() / handoff_id
    for rel in ("media", "docs", "editable", "qa", "production/payloads"):
        (run_dir / rel).mkdir(parents=True, exist_ok=True)

    manifest: dict[str, Any] = {
        "schema_version": 1,
        "return_type": "visual-production-return",
        "handoff_id": handoff_id,
        "brief_version": str(handoff.get("brief_version")),
        "skill": "aident-brand-visual-production",
        "skill_version": SKILL_VERSION,
        "mode": mode,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status_summary": "in-production",
        "assets": [],
        "docs": [],
        "blockers": [],
        "notes": "Bridge output. Visual/brand QA and pack ingest are still required.",
    }

    renderables: list[dict[str, Any]] = list(images)
    for video in videos:
        if not isinstance(video, dict):
            manifest["blockers"].append({"asset_id": "", "reason": "video deliverable must be an object", "next_action": "Fix the handoff."})
            continue
        for frame in video.get("frames") or []:
            if isinstance(frame, dict):
                merged = dict(frame)
                merged.setdefault("locale", video.get("locale") or base_payload.get("locale") or "en")
                merged.setdefault("dimensions", video.get("resolution") or "1920x1080")
                renderables.append(merged)

    for deliverable in renderables:
        if not isinstance(deliverable, dict):
            manifest["blockers"].append({"asset_id": "", "reason": "deliverable must be an object", "next_action": "Fix the handoff."})
            continue
        record, blockers = render_deliverable(
            deliverable,
            base_payload,
            copy_index,
            source_index,
            handoff_path.parent,
            run_dir,
            args.png,
        )
        manifest["assets"].append(record)
        for reason in blockers:
            manifest["blockers"].append({"asset_id": record["asset_id"], "reason": reason, "next_action": "Correct the handoff or production environment and rerun."})

    manifest["docs"] = write_video_docs(run_dir, videos)
    if manifest["blockers"]:
        manifest["status_summary"] = "mixed" if manifest["assets"] else "blocked"
    dump_yaml_compatible(run_dir / "return-manifest.yaml", manifest)
    dump_yaml_compatible(run_dir / "production" / "run-plan.json", handoff)
    (run_dir / "RETURN.md").write_text(
        "\n".join(
            [
                f"# Visual production return — {handoff_id}",
                "",
                f"- Mode: `{mode}`",
                f"- Renderable assets/frames: {len(manifest['assets'])}",
                f"- Blockers: {len(manifest['blockers'])}",
                "- Status: automated scaffold complete; visual/brand QA and pack ingest remain.",
                "- Storyboard frames are not final MP4/MOV files.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Prepared {run_dir}")
    print(f"assets={len(manifest['assets'])} blockers={len(manifest['blockers'])} png={args.png}")
    return 0 if not manifest["blockers"] else 2


if __name__ == "__main__":
    sys.exit(main())
