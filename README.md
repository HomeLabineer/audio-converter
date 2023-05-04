# Audio Converter

This is a command-line tool for converting audio files from one format to another. The tool supports batch processing of audio files in a given folder and its subfolders.

## Features

- Batch processing of audio files in a folder and its subfolders
- Supports multiple input and output formats (mp3, wma, flac, m4a)
- Selectable audio quality for output files (low, medium, high)
- Optional actions for original audio files after conversion (none, remove, or move)
- Customizable logging levels and log file path
- Status bar whilst running:
```bash
Converting:  37%|██████████████████████████████████████▍                                                                  | 787/2153 [07:51<13:23,  1.70it/s]
```

## Requirements

- Python 3.x
- ffmpy
- tqdm
- ffmpeg

## Installation

1. Clone the repository or download the script.

```bash
git clone https://github.com/yourusername/audio-converter.git
```

2. Install the required Python packages.

pip install -r requirements.txt

3. Install ffmpeg

Mac/Brew:
`brew install fmpeg`

Linux/Ubuntu/apt:

`sudo apt install ffmpeg -y`

## Usage

```bash
usage: audio_converter.py [-h] -f FOLDER_PATH [-i {wma,flac,wav,m4a}] [-o {mp3,flac,wav,m4a}] [-l LOG_FILE]
                           [-a {none,remove,move}] [-w WMA_DESTINATION] [--overwrite] [--log-level LOG_LEVEL]
                           [-q {low,medium,high}]

Convert audio files in a given folder and its subfolders.

optional arguments:
  -h, --help            show this help message and exit
  -f FOLDER_PATH, --folder-path FOLDER_PATH
                        Path to the folder containing audio files
  -i {wma,flac,wav,m4a}, --input-format {wma,flac,wav,m4a}
                        Input format for audio files (default: wma)
  -o {mp3,flac,wav,m4a}, --output-format {mp3,flac,wav,m4a}
                        Output format for converted files (default: mp3)
  -l LOG_FILE, --log-file LOG_FILE
                        Log file path (default: audio_conversion.log)
  -a {none,remove,move}, --action {none,remove,move}
                        Action for original audio files after conversion: none (default), remove, or move
  -w WMA_DESTINATION, --wma-destination WMA_DESTINATION
                        Destination folder for moved audio files (default: audio_backup)
  --overwrite           Overwrite existing output files if they already exist
  --log-level LOG_LEVEL
                        Logging level: debug, info (default), warning, error, or critical
  -q {low,medium,high}, --audio-quality {low,medium,high}
                        Audio quality for output files (default: high)
```

## Examples

1. Convert all WMA files in a folder to MP3 files with high quality:
`python audio_converter.py -f /path/to/your/folder`

2. Convert all FLAC files in a folder to M4A files with medium quality and remove the original files after conversion:

`python audio_converter.py -f /path/to/your/folder -i flac -o m4a -q medium -a remove`

## License

This project is licensed under the MIT License. See the LICENSE file for details.