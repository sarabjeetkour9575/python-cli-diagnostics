import argparse
import json
import os
import platform
import shutil
import sys
from pathlib import Path


def run_diagnostics(config_path=None):
    """Collect system diagnostics and validate an optional configuration file."""
    result = {
        "python_version": platform.python_version(),
        "operating_system": platform.system(),
        "disk_space": {},
        "environment_variables": {
            "PATH_configured": bool(os.environ.get("PATH")),
            "VIRTUAL_ENV_configured": bool(os.environ.get("VIRTUAL_ENV")),
        },
        "developer_tools": {
            "git_available": shutil.which("git") is not None,
        },
        "configuration": {
            "path": config_path,
            "valid": True,
        },
    }

    try:
        total, used, free = shutil.disk_usage(os.getcwd())
        result["disk_space"] = {
            "total_bytes": total,
            "used_bytes": used,
            "free_bytes": free,
        }
    except OSError as error:
        result["disk_space"] = {"error": str(error)}

    if config_path is not None:
        path = Path(config_path)
        if not path.exists() or not path.is_file():
            result["configuration"]["valid"] = False
            result["configuration"]["error"] = (
                "Configuration path does not exist or is not a file."
            )

    return result


def format_report(result):
    """Return a readable text version of a diagnostics result."""
    lines = [
        "=== System Diagnostics Report ===",
        f"Python Version: {result['python_version']}",
        f"Operating System: {result['operating_system']}",
    ]

    disk = result["disk_space"]
    if "free_bytes" in disk:
        lines.append(f"Free Disk Space: {disk['free_bytes']} bytes")
    else:
        lines.append(f"Disk Space Error: {disk.get('error', 'Unknown error')}")

    env = result["environment_variables"]
    lines.append(f"PATH configured: {env['PATH_configured']}")
    lines.append(f"Virtual environment configured: {env['VIRTUAL_ENV_configured']}")

    tools = result["developer_tools"]
    lines.append(f"Git available: {tools['git_available']}")

    config = result["configuration"]
    lines.append(f"Configuration valid: {config['valid']}")
    if not config["valid"]:
        lines.append(f"Configuration error: {config['error']}")

    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Inspect basic system diagnostics."
    )
    parser.add_argument(
        "--config",
        help="Optional configuration file path to validate.",
    )
    parser.add_argument(
        "--output",
        default="diagnostics_report.json",
        help="Path to save the JSON report (default: diagnostics_report.json).",
    )
    args = parser.parse_args(argv)

    result = run_diagnostics(args.config)
    print(format_report(result))

    try:
        output_path = Path(args.output)
        output_path.write_text(
            json.dumps(result, indent=4),
            encoding="utf-8",
        )
        print(f"\nJSON report saved to {output_path}")
    except OSError as error:
        print(f"Could not save JSON report: {error}", file=sys.stderr)
        return 2

    if not result["configuration"]["valid"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
