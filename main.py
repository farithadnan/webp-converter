import os
import logging
import argparse
from PIL import Image
from pathlib import Path
from datetime import datetime

def setup_logging(log_file, debug=False):
    """Configure logging to console and optionally to a file."""
    log_format = "%(asctime)s - %(levelname)s - %(message)s"

    log_file = Path(log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)  

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    logger.handlers.clear()

    # Console Handler (INFO and above)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format))

    # File Handler (DEBUG and above)
    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(log_format))

    # Attach handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    session_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    separator = f"\n========== NEW SESSION {session_time} ==========\n"
    
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(separator)

def should_skip_folder(folder_path, ignore_folders):
    """Check if a folder should be skipped based on the ignore list."""
    return any(ignore in folder_path.parts for ignore in ignore_folders)

def should_process_folder(folder_path, allow_folders):
    """Check if a folder should be processed based on the allow list."""
    return not allow_folders or any(allow in folder_path.parts for allow in allow_folders)

def convert_images_to_webp(folder, ignore_folders, allow_folders, delete_originals, dry_run):
    """Recursively find and convert images to WebP format."""
    converted, skipped = 0, 0
    folder = Path(folder)

    for root, _, files in os.walk(folder):
        root_path = Path(root)

        if should_skip_folder(root_path, ignore_folders):
            logging.debug(f"Skipping folder: {root}")
            continue
        
        if not should_process_folder(root_path, allow_folders):
            logging.debug(f"Not in allowed folders: {root}")
            continue

        for file in files:
            file_path = root_path / file
            if file_path.suffix.lower().endswith((".png", ".jpg", ".jpeg")):
                new_image_path = file_path.with_suffix(".webp")
                relative_file = file_path.relative_to(folder)
                relative_new_image = new_image_path.relative_to(folder)

                if new_image_path.exists():
                    skipped += 1
                elif dry_run:
                    logging.info(f"[DRY-RUN] Would convert: {str(relative_file):<50} → {relative_new_image}")
                    converted += 1
                else:
                    try:
                        with Image.open(file_path) as img:
                            img.save(new_image_path, "WEBP", quality=85)
                            logging.info(f"Converted: {str(relative_file):<50} → {relative_new_image}")
                            converted += 1

                        if delete_originals:
                            file_path.unlink()
                            logging.info(f"Deleted original: {relative_file}")

                    except (OSError, PermissionError) as e:
                        logging.error(f"Error converting {relative_file}: {e}")
    
    logging.info(f"=== Conversion Summary: {converted} converted, {skipped} skipped ===")



if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Convert images to WebP format recursively.")
        parser.add_argument("folder", type=Path, help="Root folder to scan for images")
        parser.add_argument("--ignore", nargs="*", default=[], help="Folders to ignore (space-separated)")
        parser.add_argument("--allow", nargs="*", default=[], help="Folders to allow (if empty, process all)")
        parser.add_argument("--delete", action="store_true", help="Delete original images after conversion")
        parser.add_argument("--dry-run", action="store_true", help="Simulate the process without making changes")
        parser.add_argument("--debug", action="store_true", help="Enable debug logging")

        args = parser.parse_args()
        setup_logging("logs/session.log", args.debug)

        logging.info(f"Starting image conversion in {args.folder}...")
        convert_images_to_webp(args.folder, args.ignore, args.allow, args.delete, args.dry_run)
    except Exception:
        logging.exception("An unexpected error occurred")

