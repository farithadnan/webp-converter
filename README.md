# WebP Image Converter

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

### Using Prebuilt Package (Recommended)
Download the latest .whl file from the [Releases section](https://github.com/farithadnan/webp-converter/releases) and install it using:
```bash
pip install path/to/webp_converter-<version>-py3-none-any.whl
```

After installation, you can use the CLI:

```bash
webp-converter <folder_path> [OPTIONS]
```
Refer to the **Usage** section for more details.

### Development Setup (Using `requirements.txt`)
For development and testing, create your `virtual env`, activate it and then install the required dependencies using:
```bash
pip install -r requirements.txt
```
This allows you to modify and run the script directly.

Run the script manually:
```bash
python main.py <folder_path> [OPTIONS]
```

### Distribution Setup (Using `setuptools` and `build`)
To package and distribute the script, activate your `virtual env` and then follow these steps:

1. Install `setuptools` and `build`:
```bash
pip install setuptools build
```

2. Build the dependencies first, go to the root folder and run this command:
```bash
pip install .
```

3. Build the distributable package:
```bash
python -m build
```
This will generate the following files inside the `dist/` folder:
- `webp_converter-<version>-py3-none-any.whl`
- `webp_converter-<version>.tar.gz`

4. Install the package locally for testing:
```bash
pip install dist/webp_converter-<version>-py3-none-any.whl
```

5. Run the installed CLI tool:
```bash
webp-converter <folder_path> [OPTIONS]
```

## Usage

### Arguments
- `<folder_path>`: The root folder to scan for images.

### Options
- `--ignore <folders path>`: Space-separated list of folders to ignore.
- `--allow <folders path>`: Space-separated list of folders to process. If omitted, all folders are processed.
- `--quality <number>`: Set WebP quality. (1-100, lower = smaller file).
- `--method <number>`: Compression method (0=fastest, 6=best).
- `--resize <width><height>`: Compression method (0=fastest, 6=best).
- `--delete`: Deletes original images after conversion.
- `--dry-run`: Simulates the process without making changes.
- `--debug`: Enables debug logging.

### Example Commands
Convert images in `./images` while ignoring `backup` and `docs` folder:
```bash
webp-converter ./images --ignore backup docs
```

Compress images in `./images`
```bash
webp-converter ./images --quality 50 --method 5 --resize 1920 1080
```

Perform a dry-run for `./photos` and only process `albums` and `images` folder:
```bash
webp-converter ./photos --allow albums images --dry-run
```

Convert and delete original images:
```bash
webp-converter ./dataset --delete
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

## Uninstalling the Package
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

