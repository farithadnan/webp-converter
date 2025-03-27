# WebP Image Converter

## Overview
This script recursively converts images in a specified folder to WebP format. It supports filtering specific folders, skipping certain directories, and optionally deleting the original images after conversion. The script also logs all activities to a log file.

## Features
- Converts `.png`, `.jpg`, and `.jpeg` images to `.webp` format.
- Recursively scans directories for images.
- Allows specifying folders to ignore or allow.
- Supports a dry-run mode to preview changes without modifying files.
- Optionally deletes original images after conversion.
- Logs operations to `logs/session.log` with timestamps.
- Includes unit tests using `pytest`.

## Requirements
- Python 3.10+
- Pillow library
- Pytest (For running tests)

## Installation

### Clone the repo
```bash
git clone https://github.com/farithadnan/webp-converter.git
cd webp-converter
```

### Manual Installation
For normal development and usage, install the required dependencies with:  
```bash
pip install -r requirements.txt
```

### Installation for Distribution
If you want to package and distribute the script, use the command below. This will generate a distributable package using `setuptools`, creating `build` and `*.egg-info folders`:
```bash
pip install .
```

## Usage
If you install the script manually, use this:
```bash
python main.py <folder_path> [OPTIONS]
```

If you install the script using setuptools, use this:
```bash
webp-converter <folder_path> [OPTIONS]
```

### Arguments
- `<folder_path>`: The root folder to scan for images.

### Options
- `--ignore <folders>`: Space-separated list of folders to ignore.
- `--allow <folders>`: Space-separated list of folders to process. If omitted, all folders are processed.
- `--delete`: Deletes original images after conversion.
- `--dry-run`: Simulates the process without making changes.
- `--debug`: Enables debug logging.

### Example Commands
Convert images in `./images` while ignoring `backup` and `docs` folder:
```bash
# Manual
python main.py ./images --ignore backup docs
# Setuptools
webp-converter main.py ./images --ignore backup docs
```

Perform a dry-run for `./photos` and only process `albums` and `images` folder:
```bash
# Manual
python main.py ./photos --allow albums images --dry-run
# Setuptools
webp-converter main.py ./photos --allow albums images --dry-run
```

Convert and delete original images:
```bash
# Manual
python main.py ./dataset --delete
# Setuptools
webp-converter main.py ./dataset --delete
```

## Running Tests
Unit tests are included and can be executed using `pytest`.

### Install `pytest`
```bash
pip install pytest
```

### Run Tests
```bash
pytest tests/
```
This will automatically discover and run all test files (`test_*.py` or `*_test.py`).

## Uninstalling Package Installed via setuptools
If installed using `pip install .`, uninstall with:
```bash
pip uninstall webp-converter -y
```

To remove the package completely, delete the project folder:
```bash
rm -rf webp-converter
```

## Logging
Logs are saved in `logs/session.log`. Each session is marked with a timestamp. Errors and conversions are recorded in the log file.

## Notes
- If `--allow` is used, only the specified folders will be processed.
- If `--dry-run` is enabled, no actual conversion or deletion will happen.
- If an error occurs, it will be logged under `logs/session.log`.

## License
This project is open-source and free to use under the [MIT License](LICENSE.md).