#!/usr/bin/env python3
"""Generate usage-scenarios-and-examples/device-catalog.md from spx-examples catalogs.

Usage:
  python scripts/generate_device_catalog.py --spx-examples ../spx-examples
  python scripts/generate_device_catalog.py --spx-examples ../spx-examples --check
"""

from __future__ import annotations

import argparse
import difflib
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List

import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--spx-examples",
        type=Path,
        default=Path("../spx-examples"),
        help="Path to local spx-examples repository (default: ../spx-examples).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("usage-scenarios-and-examples/device-catalog.md"),
        help="Output markdown path (default: usage-scenarios-and-examples/device-catalog.md).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Do not write output; fail if file content differs from generated content.",
    )
    return parser.parse_args()


def run_git(spx_examples_path: Path, args: List[str]) -> str:
    return subprocess.check_output(
        ["git", "-C", str(spx_examples_path), *args],
        text=True,
    ).strip()


def get_source_snapshot(spx_examples_path: Path) -> str:
    # Prefer origin/main to make the source-of-truth explicit.
    try:
        commit = run_git(spx_examples_path, ["rev-parse", "origin/main"])
    except subprocess.CalledProcessError:
        commit = run_git(spx_examples_path, ["rev-parse", "HEAD"])
    try:
        commit_date = run_git(spx_examples_path, ["show", "-s", "--format=%cI", commit])
    except subprocess.CalledProcessError:
        commit_date = "unknown-date"
    return f"`spx-examples` commit `{commit}` ({commit_date})"


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def make_title_case_domain_sort_key(domain_id: str, domain_name_by_id: Dict[str, str]) -> str:
    return domain_name_by_id.get(domain_id, domain_id).lower()


def detect_vendor(path: str) -> str:
    # Expected path shape: library/domains/<domain>/<vendor>/<file>.yaml
    parts = path.split("/")
    if len(parts) >= 5 and parts[0] == "library" and parts[1] == "domains":
        return parts[3]
    return "generic"


def model_filename(path: str) -> str:
    return path.split("/")[-1]


def render_catalog(spx_examples_path: Path) -> str:
    models_path = spx_examples_path / "library/catalog/models.yaml"
    industries_path = spx_examples_path / "library/catalog/industries.yaml"
    domains_path = spx_examples_path / "library/catalog/domains.yaml"

    models_data = load_yaml(models_path)["models"]
    industries_data = load_yaml(industries_path)["industries"]
    domains_data = load_yaml(domains_path)["domains"]

    domain_name_by_id = {d["id"]: d["name"] for d in domains_data}
    pack_name_by_id = {p["id"]: p["name"] for p in industries_data}
    pack_order = [p["id"] for p in industries_data]

    pack_profiles: Dict[str, set] = {}
    for pack in industries_data:
        ids = set()
        for profile_path in pack.get("profiles", []) or []:
            profile = Path(profile_path).stem
            ids.add(profile)
        pack_profiles[pack["id"]] = ids

    # pack -> domain -> vendor -> entries
    catalog = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for model in models_data:
        entry = {
            "id": model.get("id", ""),
            "name": model.get("name", ""),
            "domain": model.get("domain", ""),
            "path": model["path"],
            "filename": model_filename(model["path"]),
            "vendor": detect_vendor(model["path"]),
            "protocols": model.get("protocols", []) or [],
        }
        model_profiles = set(model.get("profiles", []) or [])

        for pack in model.get("packages", []) or []:
            entry_copy = dict(entry)
            entry_copy["profiles"] = sorted(model_profiles.intersection(pack_profiles.get(pack, set())))
            catalog[pack][entry_copy["domain"]][entry_copy["vendor"]].append(entry_copy)

    for pack_id in list(catalog.keys()):
        for domain_id in list(catalog[pack_id].keys()):
            for vendor in list(catalog[pack_id][domain_id].keys()):
                catalog[pack_id][domain_id][vendor].sort(
                    key=lambda item: (item["name"].lower(), item["filename"].lower())
                )

    snapshot = get_source_snapshot(spx_examples_path)

    lines: List[str] = []
    lines.extend(
        [
            "---",
            "description: >-",
            "  Searchable catalog of device models available per installer pack, generated from spx-examples main.",
            "icon: list",
            "---",
            "",
            "# Device Catalog (spx-examples)",
            "",
            "This page lists device models available in each installer pack.",
            "Names and file names are aligned 1:1 with `spx-examples` so docs search can find exact device strings quickly.",
            "",
            "> Important",
            "> These are reference simulation models from `spx-examples`, not official digital twins certified by device manufacturers.",
            "> They are not officially supported by manufacturers and we do not guarantee a 100% functional match to real hardware behavior.",
            "",
            f"Source snapshot: {snapshot}",
            "",
            "Generated from: `scripts/generate_device_catalog.py`.",
            "",
            "Grouping on this page: **Pack -> Domain -> Vendor/Family**.",
            "",
            "## Conventions",
            "",
            "- `Device name`: official `name` from `library/catalog/models.yaml`.",
            "- `Model file`: exact YAML file name used in the library.",
            "- `Vendor/Family`: folder under `library/domains/<domain>/...` (for example `abb`, `siemens`, `generic`).",
            "- `Profiles`: only profiles that belong to the current pack.",
            "",
        ]
    )

    for pack_id in pack_order:
        pack_entries = catalog.get(pack_id)
        if not pack_entries:
            continue

        pack_name = pack_name_by_id.get(pack_id, pack_id)
        profiles = sorted(pack_profiles.get(pack_id, set()))
        profile_text = ", ".join(f"`{p}`" for p in profiles) if profiles else "-"

        all_items: List[dict] = []
        for domain_group in pack_entries.values():
            for vendor_group in domain_group.values():
                all_items.extend(vendor_group)

        lines.append(f"## `{pack_id}` - {pack_name}")
        lines.append("")
        lines.append(f"Devices in pack: **{len(all_items)}**")
        lines.append("")
        lines.append(f"Pack profiles: {profile_text}")
        lines.append("")

        sorted_domains = sorted(
            pack_entries.keys(),
            key=lambda domain: make_title_case_domain_sort_key(domain, domain_name_by_id),
        )
        for domain_id in sorted_domains:
            domain_name = domain_name_by_id.get(domain_id, domain_id)
            domain_items: List[dict] = []
            for vendor_items in pack_entries[domain_id].values():
                domain_items.extend(vendor_items)

            lines.append(f"### Domain: `{domain_id}` - {domain_name}")
            lines.append("")
            lines.append(f"Device count in domain: **{len(domain_items)}**")
            lines.append("")

            for vendor in sorted(pack_entries[domain_id].keys(), key=str.lower):
                entries = pack_entries[domain_id][vendor]
                lines.append(f"#### Vendor/Family: `{vendor}`")
                lines.append("")
                lines.append("| Device name | Model file | Model ID | Protocols | Profiles |")
                lines.append("| --- | --- | --- | --- | --- |")
                for entry in entries:
                    url = (
                        "https://github.com/HammerHeads-Engineers/spx-examples/blob/main/"
                        f"{entry['path']}"
                    )
                    protocols = ", ".join(entry["protocols"]) if entry["protocols"] else "-"
                    profiles_cell = ", ".join(f"`{p}`" for p in entry["profiles"]) if entry["profiles"] else "-"
                    lines.append(
                        f"| {entry['name']} | [`{entry['filename']}`]({url}) | "
                        f"`{entry['id']}` | `{protocols}` | {profiles_cell} |"
                    )
                lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    repo_root = Path.cwd()
    spx_examples_path = (repo_root / args.spx_examples).resolve()
    output_path = (repo_root / args.output).resolve()

    if not spx_examples_path.exists():
        print(f"error: spx-examples path not found: {spx_examples_path}", file=sys.stderr)
        return 2
    if not (spx_examples_path / ".git").exists():
        print(f"error: not a git repository: {spx_examples_path}", file=sys.stderr)
        return 2

    generated = render_catalog(spx_examples_path)

    if args.check:
        current = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
        if current != generated:
            print(f"error: generated content differs: {output_path}", file=sys.stderr)
            diff = difflib.unified_diff(
                current.splitlines(keepends=True),
                generated.splitlines(keepends=True),
                fromfile=str(output_path),
                tofile="generated/device-catalog.md",
            )
            sys.stdout.writelines(diff)
            return 1
        print(f"ok: generated content matches: {output_path}")
        return 0

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(generated, encoding="utf-8")
    print(f"wrote: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
