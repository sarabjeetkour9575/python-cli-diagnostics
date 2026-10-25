# Python CLI Diagnostics Tool

## Overview
A command-line tool that checks basic system details and creates a JSON report.

## Features
- Python version and operating system
- Total, used, and free disk space
- `PATH` and `VIRTUAL_ENV` environment-variable checks
- Git availability check
- Optional configuration-file path validation
- Human-readable report and JSON output
- Useful exit codes

## Requirements
- Python 3.10 or later
- No third-party runtime dependencies

## Run
```bash
python main.py
python main.py --config config.json
python main.py --output report.json
python main.py --config config.json --output report.json
```

## Tests
```bash
python -m unittest -v test_diagnostics.py
```

Tests cover successful diagnostics, missing Git availability, malformed and valid configuration paths, and disk-usage error handling.

## Package installation
Use an isolated environment during development:
```bash
python -m venv .venv
```
Activate it using the command appropriate for your operating system, then run:
```bash
python -m pip install .
diagnostics
```

## Exit codes
- `0`: diagnostics completed successfully
- `1`: configuration path is invalid
- `2`: JSON report could not be saved

## Files
- `main.py`: CLI program
- `test_diagnostics.py`: unit tests
- `pyproject.toml`: package metadata and console entry point
- `README.md`: documentation
- `diagnostics_report.json`: generated report (created when the tool runs)
