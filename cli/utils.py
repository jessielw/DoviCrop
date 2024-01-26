import sys
import platform
from pathlib import Path

from cli.enums import FileType
from cli.exceptions import DoviCropFileError, DoviCropValueError


def validate_file(value: str, file_type: FileType) -> Path:
    """Validate file input/output

    Args:
        value (str): Automatically passed via argparser
        file_type (FileType): FileType.INPUT or FileType.OUTPUT

    Returns:
        Path: Path object from the input
    """
    path_obj = Path(value)
    if file_type == FileType.INPUT:
        if not path_obj.exists() or not path_obj.is_file():
            raise DoviCropFileError(f"{value} is not a valid input file")

    lower_suffix = path_obj.suffix.lower()
    if lower_suffix != ".bin":
        raise DoviCropFileError(
            f"'{lower_suffix}' is not a valid suffix. (Valid input would be 'FILENAME.bin')"
        )
    return path_obj


def validate_int(value: any) -> int:
    if value.isdigit():
        return int(value)
    else:
        raise DoviCropValueError(
            f"'{value}' is not a valid number. (Valid input would be an integer)"
        )


def exit_application(msg: str, exit_code: int = 0):
    """A clean way to exit the program without raising traceback errors

    Args:
        msg (str): Success or Error message you'd like to display in the console
        exit_code (int): Can either be 0 (success) or 1 (fail)
    """
    if exit_code not in {0, 1}:
        raise ValueError("exit_code must only be '0' or '1' (int)")

    if exit_code == 0:
        output = sys.stdout
    elif exit_code == 1:
        output = sys.stderr

    print(msg, file=output)
    sys.exit(exit_code)


def get_executable_string_by_os():
    """Check executable type based on operating system"""
    operating_system = platform.system()
    if operating_system == "Windows":
        return ".exe"
    elif operating_system == "Linux":
        return ""
