import os
import logging
import argparse
from PIL import Image
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional, Tuple

@dataclass
class ConversionSettings:
    folder: Path
    ignore_folders: List[str]
    allow_folders: List[str]
    quality: int
    method: int
    resize: Optional[Tuple[int, int]]
    delete_originals: bool
    dry_run: bool

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
    return any(ignore.lower() in map(str.lower, folder_path.parts) for ignore in ignore_folders)

def should_process_folder(folder_path, allow_folders):
    """Check if a folder should be processed based on the allow list."""
    return not allow_folders or any(allow.lower() in map(str.lower, folder_path.parts) for allow in allow_folders)

def convert_images_to_webp(settings: ConversionSettings):
    """Recursively find and convert images to WebP format."""
    converted, skipped = 0, 0
    folder = Path(settings.folder)

    for root, _, files in os.walk(folder):
        root_path = Path(root)

        if should_skip_folder(root_path, settings.ignore_folders):
            logging.debug(f"Skipping folder: {root}")
            continue
        
        if not should_process_folder(root_path, settings.allow_folders):
            logging.debug(f"Not in allowed folders: {root}")
            continue

        for file in files:
            file_path = root_path / file
            if file_path.suffix.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                new_image_path = file_path.with_suffix(".webp")
                relative_file = file_path.relative_to(folder)
                relative_new_image = new_image_path.relative_to(folder)

                if settings.dry_run:
                    logging.info(f"[DRY-RUN] Would convert: {str(relative_file):<50} → {relative_new_image}")
                    converted += 1
                else:
                    try:
                        with Image.open(file_path) as img:
                            img = img.convert("RGB")
                            
                            if settings.resize:
                                img.thumbnail(settings.resize, Image.LANCZOS)
                            
                            img.save(new_image_path, "WEBP", quality=settings.quality, optimize=True, method=settings.method)
                            logging.info(f"Converted: {str(relative_file):<50} → {relative_new_image}")
                            converted += 1

                        if settings.delete_originals and file_path.suffix.lower() not in (".webp"):
                            file_path.unlink()
                            logging.info(f"Deleted original: {relative_file}")

                    except (OSError, PermissionError) as e:
                        logging.error(f"Error converting {relative_file}: {e}")
            else:
                logging.debug(f"Skipping non-targeted file: {file_path}")
    
    logging.info(f"=== Conversion Summary: {converted} converted, {skipped} skipped ===")

def main():
    """Entry point for CLI execution."""
    try:
        parser = argparse.ArgumentParser(description="Convert images to WebP format recursively.")
        parser.add_argument("folder", type=Path, help="Root folder to scan for images")
        parser.add_argument("--ignore", nargs="*", default=[], help="Folders to ignore (space-separated)")
        parser.add_argument("--allow", nargs="*", default=[], help="Folders to allow (if empty, process all)")
        parser.add_argument("--quality", type=int, default=75, help="Set WebP quality (1-100, lower = smaller file)")
        parser.add_argument("--method", type=int, choices=range(0, 7), default=6, help="Compression method (0=fastest, 6=best)")
        parser.add_argument("--resize", type=int, nargs=2, metavar=("WIDTH", "HEIGHT"), help="Resize images before conversion")
        parser.add_argument("--delete", action="store_true", help="Delete original images after conversion")
        parser.add_argument("--dry-run", action="store_true", help="Simulate the process without making changes")
        parser.add_argument("--debug", action="store_true", help="Enable debug logging")

        args = parser.parse_args()
        setup_logging("logs/session.log", args.debug)

        settings = ConversionSettings(
            folder=args.folder,
            ignore_folders=args.ignore,
            allow_folders=args.allow,
            quality=args.quality,
            method=args.method,
            resize=tuple(args.resize) if args.resize else None,
            delete_originals=args.delete,
            dry_run=args.dry_run
        )

        logging.info(f"Starting image conversion in {settings.folder}...")
        convert_images_to_webp(settings)
    except Exception:
        logging.exception("An unexpected error occurred")

if __name__ == "__main__":
    main()
