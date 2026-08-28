#!/usr/bin/env python3
"""
Trade OS — ai_context regenerator
Reads CODEMAP.json and regenerates ai_context/INDEX.md + ai_context/modules/MODULE_*.md

Usage:
    python update.py                   # full regeneration
    python update.py --module scoring  # regenerate one module only
    python update.py --check           # validate CODEMAP.json, write nothing
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent
CODEMAP_PATH = ROOT / "CODEMAP.json"
AI_CONTEXT = ROOT / "ai_context"
MODULES_DIR = AI_CONTEXT / "modules"

# Map every module ID → file slug (must match CODEMAP.json module IDs)
MODULE_SLUG = {
    "M1_infra":       "infra",
    "M2_schema":      "schema",
    "M3_seed":        "seed",
    "M4_scoring":     "scoring",
    "M5_api":         "api",
    "M6_match_ui":    "match_ui",
    "M7_signals_ui":  "signals_ui",
    "M8_account_ui":  "account_ui",
    "M9_data_expand": "data_expand",
    "M10_search":     "search",
    "M11_agents":     "agents",
}

LAYER_SECTIONS = [
    ("DB",  "DB Models"),
    ("SVC", "Service Functions"),
    ("REP", "Repository Functions"),
    ("RTE", "API Routes"),
    ("SCH", "Pydantic Schemas"),
    ("WRK", "Background Workers"),
    ("FE",  "Frontend Components"),
    ("INF", "Infrastructure Files"),
    ("TST", "Tests"),
]

STATUS_ICON = {
    "NOT_STARTED": "[ ]",
    "IN_PROGRESS": "[/]",
    "DONE":        "[x]",
}


def load_codemap() -> dict:
    if not CODEMAP_PATH.exists():
        print(f"ERROR: CODEMAP.json not found at {CODEMAP_PATH}")
        sys.exit(1)
    with open(CODEMAP_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_codemap(data: dict) -> None:
    with open(CODEMAP_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def validate_codemap(data: dict) -> list[str]:
    errors = []
    meta = data.get("meta", {})
    if not meta.get("project"):
        errors.append("meta.project is missing")
    if not meta.get("entity_code_format"):
        errors.append("meta.entity_code_format is missing")
    modules = data.get("modules", {})
    for mid, mod in modules.items():
        if mid not in MODULE_SLUG:
            errors.append(f"Module {mid} not in MODULE_SLUG dict in update.py")
        if not mod.get("slug"):
            errors.append(f"Module {mid} missing slug")
        if mod.get("status") not in ("NOT_STARTED", "IN_PROGRESS", "DONE"):
            errors.append(f"Module {mid} has invalid status: {mod.get('status')}")
    return errors


def get_entities_for_module(entities: dict, module_slug: str) -> dict[str, list[dict]]:
    """Group entities for a given module by layer code."""
    result: dict[str, list[dict]] = {layer: [] for layer, _ in LAYER_SECTIONS}
    for code, entity in entities.items():
        parts = code.split("-")
        if len(parts) < 3:
            continue
        layer = parts[1]
        entity_module = parts[2]
        # Match module slug or shared
        mod_slug = MODULE_SLUG.get(f"M{_find_module_number(entity_module)}_")
        # Simple: check if the entity's module code appears in the slug
        slug_upper = module_slug.upper().replace("_", "")
        entity_module_upper = entity_module.upper().replace("_", "")
        if entity_module_upper == slug_upper or entity_module == "SHR":
            if layer in result:
                result[layer].append({"code": code, **entity})
    return result


def _find_module_number(module_code: str) -> str:
    """Not needed in simple approach; kept for future use."""
    return ""


def get_entities_for_module_simple(entities: dict, module_slug: str) -> dict[str, list[dict]]:
    """Group entities for a given module slug by layer code."""
    slug_map = {v.upper(): k for k, v in MODULE_SLUG.items()}
    result: dict[str, list[dict]] = {layer: [] for layer, _ in LAYER_SECTIONS}
    for code, entity in entities.items():
        parts = code.split("-")
        if len(parts) < 4:
            continue
        layer = parts[1]
        mod_code = parts[2]
        if layer in result:
            # match if mod_code matches slug (case-insensitive)
            if mod_code.upper() == module_slug.upper().replace("_", ""):
                result[layer].append({"code": code, **entity})
    return result


def generate_module_file(module_id: str, module: dict, entities: dict, slug: str) -> str:
    lines = [
        f"# MODULE_{slug} — {module['name']}",
        f"**Sprint:** {module['sprint']} | **Status:** {module['status']} | **Module ID:** {module_id}",
        "",
        f"## Description",
        module.get("description", "_No description._"),
        "",
    ]

    by_layer = get_entities_for_module_simple(entities, slug)

    for layer_code, layer_name in LAYER_SECTIONS:
        layer_entities = by_layer.get(layer_code, [])
        lines.append(f"## {layer_name}")
        if not layer_entities:
            lines.append("_No entities registered yet._")
        else:
            lines.append("| Code | Name | Description |")
            lines.append("|------|------|-------------|")
            for e in layer_entities:
                name = e.get("name", "")
                desc = e.get("description", "")
                lines.append(f"| {e['code']} | {name} | {desc} |")
        lines.append("")

    lines.append("---")
    lines.append(f"*Auto-generated by update.py — do not edit manually.*")
    lines.append(f"*Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}*")
    return "\n".join(lines)


def generate_index(data: dict) -> str:
    meta = data["meta"]
    modules = data["modules"]
    entities = data.get("entities", {})
    dep_rules = data.get("dependency_rules", {})

    lines = [
        f"# Trade OS — Module Index",
        f"*Project: {meta['project']} | Sprint: {meta['active_sprint']} | "
        f"Total Entities: {meta.get('total_entities', 0)} | "
        f"Updated: {meta.get('last_updated', 'never')}*",
        "",
        "## Module Status",
        "",
        "| # | Module | Slug | Sprint | Status |",
        "|---|--------|------|--------|--------|",
    ]

    for mid, mod in modules.items():
        icon = STATUS_ICON.get(mod["status"], "⬜")
        lines.append(
            f"| {mid} | {mod['name']} | {mod['slug']} | {mod['sprint']} | {icon} {mod['status']} |"
        )

    lines += [
        "",
        "## Shared Utilities",
        "",
        "| Code | Name | File | Purpose |",
        "|------|------|------|---------|",
    ]

    shared_utl = {k: v for k, v in entities.items() if "-SHR-" in k or "-UTL-SHR-" in k}
    if shared_utl:
        for code, e in shared_utl.items():
            lines.append(f"| {code} | {e.get('name','')} | {e.get('file','')} | {e.get('description','')} |")
    else:
        lines.append("| — | require_api_key | backend/app/api/deps.py | Auth |")
        lines.append("| — | get_db | backend/app/database.py | DB session |")
        lines.append("| — | grade_from_score | backend/app/services/scoring_service.py | Grading |")

    lines += [
        "",
        "## Config Keys",
        "",
        "| Code | Key |",
        "|------|-----|",
    ]
    cfg_entities = {k: v for k, v in entities.items() if "-CFG-" in k}
    if cfg_entities:
        for code, e in cfg_entities.items():
            lines.append(f"| {code} | {e.get('name', '')} |")
    else:
        for key in ["DATABASE_URL", "ENVIRONMENT", "API_KEY", "OPENAI_API_KEY"]:
            lines.append(f"| — | {key} |")

    if dep_rules:
        lines += [
            "",
            "## Dependency Rules",
            "",
        ]
        for i, (key, rule) in enumerate(dep_rules.items(), 1):
            lines.append(f"{i}. {rule}")

    lines += [
        "",
        "---",
        f"*Auto-generated by update.py — do not edit manually.*",
    ]
    return "\n".join(lines)


def count_entities(entities: dict) -> int:
    return len(entities)


def run(args) -> None:
    data = load_codemap()

    # Validate
    errors = validate_codemap(data)
    if errors:
        print("CODEMAP.json validation errors:")
        for e in errors:
            print(f"  ✗ {e}")
        if args.check:
            sys.exit(1)
        else:
            print("WARNING: continuing with errors")

    if args.check:
        print("[OK] CODEMAP.json is valid")
        print(f"  Project: {data['meta']['project']}")
        print(f"  Modules: {len(data['modules'])}")
        print(f"  Entities: {count_entities(data.get('entities', {}))}")
        return

    # Update meta
    data["meta"]["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    data["meta"]["last_updated_by"] = "update.py"
    data["meta"]["total_entities"] = count_entities(data.get("entities", {}))

    entities = data.get("entities", {})
    modules = data.get("modules", {})
    files_written = []

    AI_CONTEXT.mkdir(exist_ok=True)
    MODULES_DIR.mkdir(exist_ok=True)

    # Generate INDEX.md
    if not args.module:
        index_content = generate_index(data)
        index_path = AI_CONTEXT / "INDEX.md"
        index_path.write_text(index_content, encoding="utf-8")
        files_written.append(str(index_path))

    # Generate MODULE files
    for mid, mod in modules.items():
        slug = MODULE_SLUG.get(mid)
        if not slug:
            print(f"  WARNING: {mid} not in MODULE_SLUG, skipping")
            continue
        if args.module and args.module != slug:
            continue
        content = generate_module_file(mid, mod, entities, slug)
        out_path = MODULES_DIR / f"MODULE_{slug}.md"
        out_path.write_text(content, encoding="utf-8")
        files_written.append(str(out_path))

    # Always generate MODULE_shared.md
    if not args.module or args.module == "shared":
        shared_content = generate_shared_module(entities)
        shared_path = MODULES_DIR / "MODULE_shared.md"
        shared_path.write_text(shared_content, encoding="utf-8")
        files_written.append(str(shared_path))

    # Save updated meta back to CODEMAP.json
    save_codemap(data)

    # Summary
    print(f"\n[OK] Trade OS ai_context updated")
    print(f"  Files written: {len(files_written)}")
    print(f"  Entities: {data['meta']['total_entities']}")
    print(f"  Active sprint: {data['meta']['active_sprint']}")
    print(f"  Modules: {len(modules)}")
    if files_written:
        for f in files_written:
            print(f"    -> {Path(f).name}")


def generate_shared_module(entities: dict) -> str:
    shared = {k: v for k, v in entities.items() if "-SHR-" in k}
    lines = [
        "# MODULE_shared — Shared Utilities",
        "**Status:** ALWAYS LOAD | **Type:** UTL / CFG",
        "",
        "## Purpose",
        "Shared utilities, dependencies, config keys, and UI components used across all modules.",
        "",
        "## Entity Code Format",
        "```",
        "Format: TOS-{LAYER}-{MODULE}-{SEQ}",
        "",
        "LAYER: DB SVC REP RTE SCH WRK UTL CFG FE INF TST",
        "MODULE: INFRA SCHEMA SEED SCORING API MATCH SIG ACC DATA SEARCH AGENTS SHR",
        "SEQ: 3-digit zero-padded, assigned in order of creation per LAYER+MODULE",
        "```",
        "",
    ]

    if shared:
        lines.append("## Registered Shared Entities")
        lines.append("| Code | Name | File | Description |")
        lines.append("|------|------|------|-------------|")
        for code, e in shared.items():
            lines.append(f"| {code} | {e.get('name','')} | {e.get('file','')} | {e.get('description','')} |")
    else:
        lines.append("## Core Shared Utilities (pre-registered)")
        lines.append("| Code | Name | File |")
        lines.append("|------|------|------|")
        for name, file in [
            ("require_api_key", "backend/app/api/deps.py"),
            ("get_db", "backend/app/database.py"),
            ("grade_from_score", "backend/app/services/scoring_service.py"),
            ("set_updated_at", "backend/sql/003_functions.sql"),
        ]:
            lines.append(f"| — | {name} | {file} |")

    lines += [
        "",
        "---",
        "*Auto-generated by update.py — do not edit manually.*",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Trade OS ai_context regenerator")
    parser.add_argument(
        "--module",
        type=str,
        default=None,
        help="Regenerate a single module by slug (e.g. scoring, api, match_ui)"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate CODEMAP.json without writing files"
    )
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
