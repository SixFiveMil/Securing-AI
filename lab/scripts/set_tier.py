#!/usr/bin/env python3
"""Switch Blue Team rule tiers by copying a preset into filter_rules.py."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


TIER_MAP = {
    "calibrated": "rules_calibrated.py",
    "demo": "rules_calibrated.py",
    "scaffolded": "rules_scaffolded.py",
    "student": "rules_scaffolded.py",
    "blank": "rules_blank.py",
    "advanced": "rules_blank.py",
}

CANONICAL_TIER = {
    "rules_calibrated.py": "calibrated",
    "rules_scaffolded.py": "scaffolded",
    "rules_blank.py": "blank",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Set the active Blue Team rule tier for the gateway."
    )
    parser.add_argument(
        "tier",
        nargs="?",
        default="calibrated",
        help=(
            "Tier name: calibrated|demo, scaffolded|student, blank|advanced "
            "(default: calibrated)."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    requested_tier = args.tier.strip().lower()

    preset_filename = TIER_MAP.get(requested_tier)
    if preset_filename is None:
        valid = "calibrated (demo), scaffolded (student), blank (advanced)"
        print(f"Error: unknown tier '{args.tier}'.")
        print(f"Valid options: {valid}")
        return 2

    script_dir = Path(__file__).resolve().parent
    lab_dir = script_dir.parent
    preset_path = lab_dir / "presets" / preset_filename
    destination_path = script_dir / "filter_rules.py"

    if not preset_path.exists():
        print(f"Error: preset file not found: {preset_path}")
        return 1

    shutil.copyfile(preset_path, destination_path)
    active_tier = CANONICAL_TIER[preset_filename]

    print(f"Active rule tier: {active_tier}")
    print(f"Copied: {preset_path}")
    print(f"To:     {destination_path}")
    print(
        "Reminder: secure_gateway.py hot-reloads filter_rules.py on each request; "
        "no Docker restart is needed to apply rule edits."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())