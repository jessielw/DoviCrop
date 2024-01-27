import json
from argparse import ArgumentParser
from pathlib import Path
import subprocess as sp

from cli.exceptions import (
    DoviCropRPUError,
    DoviCropJSONError,
    DoviCropValueError,
    DoviCropKeyError,
)
from cli.utils import exit_application


class ProcessJob:
    def __init__(self, args: ArgumentParser.parse_args):
        self.args = args
        self.check_rpu(args.input, exit_on_success=args.check)
        ar_json = self.export_active_areas()
        applied_crops = self.apply_crops(ar_json)
        modified_json = self.set_mode(applied_crops)
        write_cropped_json = self.write_modified_json(modified_json)
        self.modified_rpu = self.modify_rpu(write_cropped_json)
        self.clean_up([self.args.input, ar_json, write_cropped_json])

    def check_rpu(self, file_path: Path, exit_on_success: bool):
        """Basic check to see if the RPU has ANY data inside of it"""
        rpu_size = file_path.stat().st_size
        if rpu_size == 0:
            DoviCropRPUError(
                f"{file_path.name} is 0 bytes, this indicates a broken RPU file"
            )
        else:
            if exit_on_success:
                exit_application("RPU is valid", 0)

    def export_active_areas(self) -> Path:
        """Uses dovi_tool to extract the active area data to JSON"""
        ar_json = self.args.output.with_name(self.args.output.stem + "_exp_ar.json")
        command = [
            str(self.args.dovi_tool),
            "export",
            "--data",
            f"level5={ar_json}",
            "-i",
            str(self.args.input),
        ]
        job = sp.run(command, check=True)
        if job.returncode == 0 and ar_json.exists():
            return ar_json
        else:
            raise DoviCropJSONError("Error exporting active area data")

    def apply_crops(self, ar_json: Path) -> dict:
        """Applies crops and adds crop key if needed"""
        try:
            with open(ar_json, "r") as json_file:
                rpu_dict = json.load(json_file)
                rpu_dict.update({"crop": True})
                json_dict = {"active_area": rpu_dict}

                # Check if "presets" key exists
                presets = json_dict["active_area"].get("presets", [])
                if not presets:
                    raise DoviCropKeyError("No 'presets' found in the JSON file")

                for preset in presets:
                    left = preset.get("left", 0) - self.args.left_crop
                    right = preset.get("right", 0) - self.args.right_crop
                    top = preset.get("top", 0) - self.args.top_crop
                    bottom = preset.get("bottom", 0) - self.args.bottom_crop

                    # Check for negative crop values
                    if any(value < 0 for value in [left, right, top, bottom]):
                        raise DoviCropValueError("Negative crop values are not allowed")

                    # Update preset values
                    preset["left"] = left
                    preset["right"] = right
                    preset["top"] = top
                    preset["bottom"] = bottom

            return json_dict

        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise DoviCropJSONError(f"Error processing JSON file '{ar_json}': {e}")

    def set_mode(self, json_dict: dict):
        """Sets dovi_tool mode"""
        json_dict.update({"mode": self.args.mode})
        return json_dict

    def write_modified_json(self, json_dict: dict) -> Path:
        """Writes modified JSON to file"""
        cropped_json = self.args.output.with_name(
            self.args.output.stem + "_crop_ar.json"
        )
        with open(cropped_json, "w+") as json_file:
            json_file.write(json.dumps(json_dict, indent=2))
        if cropped_json.exists():
            return cropped_json
        else:
            raise DoviCropJSONError("Failed to write cropped JSON")

    def modify_rpu(self, cropped_json: Path) -> Path:
        """Modifies original RPU with modified JSON"""
        command = [
            str(self.args.dovi_tool),
            "editor",
            "-i",
            str(self.args.input),
            "-j",
            str(cropped_json),
            "-o",
            str(self.args.output),
        ]
        job = sp.run(command, check=True)
        if job.returncode == 0 and self.args.output.exists():
            return self.args.output
        else:
            raise DoviCropJSONError("Error writing modified RPU")

    def clean_up(self, files: list):
        """Automatically cleans up unless the user decides not to"""
        if not self.args.no_clean_up:
            for f in files:
                Path(f).unlink(missing_ok=True)
