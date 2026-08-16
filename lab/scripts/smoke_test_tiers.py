#!/usr/bin/env python3
"""Tiny smoke test for tier switching and filter_rules import sanity."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path


ALIASES = {
    "calibrated": "rules_calibrated.py",
    "demo": "rules_calibrated.py",
    "scaffolded": "rules_scaffolded.py",
    "student": "rules_scaffolded.py",
    "blank": "rules_blank.py",
    "advanced": "rules_blank.py",
}


def run_set_tier(repo_root: Path, tier: str) -> None:
    script = repo_root / "lab" / "scripts" / "set_tier.py"
    result = subprocess.run(
        [sys.executable, str(script), tier],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"set_tier failed for '{tier}' (exit {result.returncode})\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )


def import_filter_rules(filter_rules_path: Path, tier: str) -> object:
    module_name = f"filter_rules_smoke_{tier}"
    spec = importlib.util.spec_from_file_location(module_name, filter_rules_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to build import spec for {filter_rules_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_rule_shapes(module: object, tier: str) -> None:
    for attr in ("INGRESS_BLACKLIST", "EGRESS_SECRETS", "EGRESS_PATTERNS"):
        value = getattr(module, attr, None)
        if not isinstance(value, list):
            raise AssertionError(f"{tier}: {attr} is not a list")


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    presets_dir = repo_root / "lab" / "presets"
    filter_rules_path = repo_root / "lab" / "scripts" / "filter_rules.py"
    original_contents = filter_rules_path.read_text(encoding="utf-8")

    try:
        for tier, preset_name in ALIASES.items():
            run_set_tier(repo_root, tier)

            expected = (presets_dir / preset_name).read_text(encoding="utf-8")
            actual = filter_rules_path.read_text(encoding="utf-8")
            if actual != expected:
                raise AssertionError(
                    f"{tier}: copied filter_rules.py does not match {preset_name}"
                )

            module = import_filter_rules(filter_rules_path, tier)
            assert_rule_shapes(module, tier)

        print("Smoke test passed: tier copy and filter_rules import checks are healthy.")
        return 0
    finally:
        filter_rules_path.write_text(original_contents, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())