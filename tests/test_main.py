import re
import pytest
import logging
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
from main import should_skip_folder, should_process_folder, convert_images_to_webp, setup_logging

@pytest.mark.parametrize("folder_path, ignore_folders, expected", [
    (Path("/images/photos"), ["photos"], True),
    (Path("/images/docs"), ["photos"], False),
    (Path("/images/photos/sub"), ["photos"], True),
])
def test_should_skip_folder(folder_path, ignore_folders, expected):
    assert should_skip_folder(folder_path, ignore_folders) == expected

@pytest.mark.parametrize("folder_path, allow_folders, expected", [
    (Path("/images/photos"), ["photos"], True),
    (Path("/images/docs"), ["photos"], False),
    (Path("/images"), [], True),
])
def test_should_process_folder(folder_path, allow_folders, expected):
    assert should_process_folder(folder_path, allow_folders) == expected

@patch("main.Image.open")
@patch("main.Path.unlink")
@patch("main.os.walk")
def test_convert_images_to_webp(mock_os_walk, mock_unlink, mock_image_open):
    mock_os_walk.return_value = [("/images", [], ["test.jpg", "skip.txt"])]
    mock_image = MagicMock()
    mock_image_open.return_value.__enter__.return_value = mock_image

    with patch("main.logging.info") as mock_log_info:
        convert_images_to_webp("/images", ignore_folders=[], allow_folders=[], delete_originals=True, dry_run=False)
        
        mock_image.save.assert_called_once_with(Path("/images/test.webp"), "WEBP", quality=85)
        mock_unlink.assert_called_once_with()
        
        # Debugging output
        print(mock_log_info.call_args_list)

        # Flexible assertion
        assert any(re.search(r"Converted:\s*test.jpg\s*→\s*test.webp", call[0][0]) for call in mock_log_info.call_args_list)
        assert any("Deleted original: test.jpg" in call[0][0] for call in mock_log_info.call_args_list)


@patch("main.logging.FileHandler")
@patch("main.Path.mkdir")
def test_setup_logging(mock_mkdir, mock_file_handler):
    with patch("main.logging.getLogger") as mock_get_logger:
        setup_logging("logs/test.log", debug=True)
        
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_get_logger.return_value.setLevel.assert_called_once_with(logging.DEBUG)
        mock_file_handler.assert_called_once()
