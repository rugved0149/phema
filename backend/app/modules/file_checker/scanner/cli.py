"""
Command-line interface for PHEMA File Checker Module.

This module performs static file analysis and emits standardized
PHEMA-compatible detection events.

It does NOT:
- compute overall risk
- classify files as malicious
- perform correlation
- make blocking decisions

Author: Rugved Suryawanshi
"""

import argparse
import sys
from pathlib import Path

from app.modules.file_checker.scanner.scanner import scan_file
from app.modules.file_checker.scanner.utils import write_json
from app.modules.file_checker.scanner.rules_loader import check_yara_installation, get_installation_help
from app.modules.file_checker.  scanner.event_adapter import convert_analysis_to_events


def main():
    parser = argparse.ArgumentParser(
        description="PHEMA File Checker — Static Detection Module",
        epilog="Example: python -m scanner.cli sample_files --recursive"
    )

    parser.add_argument(
        "path",
        help="File or directory to analyze"
    )

    parser.add_argument(
        "-o", "--output",
        default="outputs/events.json",
        help="Output JSON file for emitted events (default: outputs/events.json)"
    )

    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Scan directories recursively"
    )

    parser.add_argument(
        "--check-yara",
        action="store_true",
        help="Check YARA installation and exit"
    )

    args = parser.parse_args()

    # ---- YARA Check ----
    if args.check_yara:
        if check_yara_installation():
            print("✓ YARA is properly installed")
            return 0
        else:
            print("✗ YARA is not installed or not accessible")
            print(get_installation_help())
            return 1

    target = Path(args.path)

    if not target.exists():
        print(f"ERROR: Path does not exist: {target}")
        return 1

    all_events = []

    try:
        # ---- Scan Single File ----
        if target.is_file():
            raw_result = scan_file(str(target))
            events = convert_analysis_to_events(raw_result)
            all_events.extend(events)

        # ---- Scan Directory ----
        else:
            files = target.rglob("*") if args.recursive else target.iterdir()

            for file in files:
                if file.is_file():
                    raw_result = scan_file(str(file))
                    events = convert_analysis_to_events(raw_result)
                    all_events.extend(events)

        # ---- Write Events ----
        write_json(all_events, args.output)

        print(f"\nAnalysis complete. Events emitted: {len(all_events)}")
        print(f"Events written to: {args.output}")

        return 0

    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user")
        return 130

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
