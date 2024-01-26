import argparse

from cli._version import program_name, __version__
from cli.utils import validate_file, validate_int, exit_application
from cli.enums import FileType
from cli.process import ProcessJob


def main():
    parser = argparse.ArgumentParser(prog=program_name)
    parser.add_argument(
        "-v", "--version", action="version", version=f"{program_name} v{__version__}"
    )
    parser.add_argument(
        "-i",
        "--input",
        type=lambda v: validate_file(v, FileType.INPUT),
        help="Input file (i.e. rpu.bin)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=lambda v: validate_file(v, FileType.OUTPUT),
        help="Output file (i.e. rpu_out.bin)",
    )
    parser.add_argument(
        "-l", "--left-crop", default=0, type=validate_int, help="Left crop"
    )
    parser.add_argument(
        "-r", "--right-crop", default=0, type=validate_int, help="Right crop"
    )
    parser.add_argument(
        "-t", "--top-crop", default=0, type=validate_int, help="Top crop"
    )
    parser.add_argument(
        "-b", "--bottom-crop", default=0, type=validate_int, help="Bottom crop"
    )
    parser.add_argument(
        "-m",
        "--mode",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4, 5],
        help="Set mode for RPU",
    )
    parser.add_argument(
        "-c",
        "--check",
        action="store_true",
        help="Checks input RPU to see if it has valid metadata and exits the application",
    )
    parser.add_argument(
        "-d",
        "--dovi-tool",
        help="Path to dovi_tool executable",
    )
    parser.add_argument(
        "--no-clean-up",
        action="store_true",
        help="Prevents removal of JSON files created during the job process",
    )

    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        exit_application("\nError: -i/--input is required", 1)

    if not args.dovi_tool:
        parser.print_help()
        exit_application("\nError: -d/--dovi-tool is required", 1)

    try:
        ProcessJob(args)
    except Exception as e:
        exit_application(f"Error {e}", 1)
