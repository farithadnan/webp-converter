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

## Requirements
- Python 3.10+
- Pillow library

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage
```bash
python main.py <folder_path> [OPTIONS]
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
python main.py ./images --ignore backup docs
```

Perform a dry-run for `./photos` and only process `albums` and `images` folder:
```bash
python main.py ./photos --allow albums images --dry-run
```

Convert and delete original images:
```bash
python main.py ./dataset --delete
```

## Logging
Logs are saved in `logs/session.log`. Each session is marked with a timestamp. Errors and conversions are recorded in the log file.

## Notes
- If `--allow` is used, only the specified folders will be processed.
- If `--dry-run` is enabled, no actual conversion or deletion will happen.
- If an error occurs, it will be logged under `logs/session.log`.

## License
This project is open-source and free to use under the [MIT License](LICENSE.md).
