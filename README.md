# DoviCrop

Utility designed to assist the user in properly cropping their extracted dolby vision RPU for use with HEVC/x265.

## Install (portable)

You can either use it as a script in Python or download/build the exe for your platform.

## Requires

It depends on the path to `dovi_tool` being fed via an argument. You can get dovi_tool here https://github.com/quietvoid/dovi_tool.

## Usage

```
usage: DoviCrop [-h] [-v] [-i INPUT] [-o OUTPUT] [-l LEFT_CROP] [-r RIGHT_CROP] [-t TOP_CROP]
                [-b BOTTOM_CROP] [-m {0,1,2,3,4,5}] [-c] [-d DOVI_TOOL] [--no-clean-up]

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -i INPUT, --input INPUT
                        Input file (i.e. rpu.bin)
  -o OUTPUT, --output OUTPUT
                        Output file (i.e. rpu_out.bin)
  -l LEFT_CROP, --left-crop LEFT_CROP
                        Left crop
  -r RIGHT_CROP, --right-crop RIGHT_CROP
                        Right crop
  -t TOP_CROP, --top-crop TOP_CROP
                        Top crop
  -b BOTTOM_CROP, --bottom-crop BOTTOM_CROP
                        Bottom crop
  -m {0,1,2,3,4,5}, --mode {0,1,2,3,4,5}
                        Set mode for RPU
  -c, --check           Checks input RPU to see if it has valid metadata and exits the
                        application
  -d DOVI_TOOL, --dovi-tool DOVI_TOOL
                        Path to dovi_tool executable
  --no-clean-up         Prevents removal of temporary files created during the job process
```

## Example

```
"RPU.bin" -d "dovi_tool.exe" -m 2 -t 20 -b 20
```
