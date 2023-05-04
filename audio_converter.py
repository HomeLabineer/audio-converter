"""
audio_converter.py: Recursively convert audio files in a directory and its subfolders from one format to another

------------------------------
Audio Converter Info
------------------------------
Copyright (C) 2023 HomeLabineer
This project is licensed under the MIT License. See the LICENSE file for details.
Script Name: audio_converter.py
Description: A script to recursively convert audio files in a directory and its subfolders from one format to another.
             The script supports multiple audio formats and quality options, and can perform actions on the original
             files after conversion, such as removal or moving them to a backup folder.

Usage:
  1. Configure the script by setting the necessary options using command-line arguments.
  2. Save the script as audio_converter.py.
  3. Make sure to install the required Python libraries: ffmpy, tqdm, and concurrent.futures.
  4. Run the script with the desired options: python3 audio_converter.py --folder-path /path/to/folder --input-format wma --output-format mp3

Command-Line Arguments:
  -f, --folder-path: Path to the folder containing audio files.
  -i, --input-format: Input format for audio files (default: wma).
  -o, --output-format: Output format for converted files (default: mp3).
  -l, --log-file: Path to the log file (default: audio_conversion.log).
  -a, --action: Action for original audio files after conversion: none (default), remove, or move.
  -w, --wma-destination: Destination folder for moved audio files (default: audio_backup).
  --overwrite: Overwrite existing output files if they already exist.
  --log-level: Logging level: debug, info (default), warning, error, or critical.
"""


import os
from os import remove
import shutil
import logging
import argparse
from ffmpy import FFmpeg, FFRuntimeError
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from tqdm import tqdm

# Define audio formats and quality options
AUDIO_QUALITY = {
    # Add more audio formats and quality presets as needed...
    "mp3": {
        "codec": "libmp3lame",
        "options": {
            "low": "-q 5",
            "medium": "-q 2",
            "high": "-b:a 320k",
        },
    },
    "wma": {
        "codec": "wmav2",
        "options": {
            "low": "-b:a 64k",
            "medium": "-b:a 128k",
            "high": "-b:a 192k",
        },
    },
    "flac": {
        "codec": "flac",
        "options": {
            "low": "-compression_level 1",
            "medium": "-compression_level 5",
            "high": "-compression_level 8",
        },
    },
    "m4a": {
        "codec": "aac",
        "options": {
            "low": "-b:a 64k",
            "medium": "-b:a 128k",
            "high": "-b:a 256k",
        },
    },
    # Add more audio formats and quality presets here...
}

def find_audio_files(dir_path, input_format):
    # Find audio files with a specific format in a directory and its subdirectories
    audio_files = []

    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.lower().endswith(f'.{input_format.lower()}'):
                file_path = os.path.join(root, file)
                audio_files.append(file_path)

    return audio_files


def convert_audio(input_file, output_format, input_format, audio_quality, overwrite):
    # Convert an audio file from one format to another
    output_file = input_file[:-len(input_format)] + f'.{output_format}'
    
    if os.path.exists(output_file) and not overwrite:
        return (False, (input_file, output_file))

    codec = AUDIO_QUALITY[output_format]["codec"]
    ffmpeg_options = f'-loglevel panic -y {AUDIO_QUALITY[output_format]["options"][audio_quality]} -acodec {codec}'

    ff = FFmpeg(inputs={input_file: None}, outputs={output_file: ffmpeg_options})
    try:
        ff.run()
    except FFRuntimeError as e:
        return (False, f"{input_file}: {str(e)}")
    return (True, (input_file, output_file))


def main(args):
    # Parse and assign command-line arguments
    folder_path = args.folder_path
    input_format = args.input_format
    output_format = args.output_format
    audio_quality = args.audio_quality
    log_file = args.log_file
    action = args.action
    wma_destination = args.wma_destination
    overwrite = args.overwrite
    log_level = args.log_level.upper()

    if input_format == output_format:
        logging.error("Input and output formats are the same. Conversion not needed.")
        return

    # Parse and assign command-line arguments
    log_level_obj = getattr(logging, log_level, None)
    if not isinstance(log_level_obj, int):
        raise ValueError(f"Invalid log level: {log_level}")

    logging.basicConfig(level=log_level_obj, format='%(asctime)s - %(levelname)s - %(message)s', filename=log_file)

    # Start the script and log the beginning
    logging.info("Script started")

    # Scan for and count the number of input format files
    logging.info(f"Scanning {folder_path} for {input_format.upper()} files")
    audio_files = find_audio_files(folder_path, input_format)
    # If no input format files found, log a warning and exit
    if not audio_files:
        logging.warning(f"No {input_format.upper()} files found.")
        return

    logging.info(f"Found {len(audio_files)} {input_format.upper()} files. Converting to {output_format.upper()}...")

    # Convert the input format files to the output format using a ThreadPoolExecutor

    with ThreadPoolExecutor() as executor:
        futures = []
        for input_file in audio_files:
            futures.append(executor.submit(convert_audio, input_file, output_format, input_format, audio_quality, overwrite))

        # Iterate over the completed futures, handling the results
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Converting"):
            success, result = future.result()

            if success:
                input_file, output_file = result

                input_size = os.path.getsize(input_file)
                output_size = os.path.getsize(output_file)
                logging.info(f"Converted {input_file} ({input_size} bytes) to {output_file} ({output_size} bytes)")
                
                if action == "remove":
                    remove(input_file)
                    logging.info(f"Deleted original {input_format.upper()} file: {input_file}")
                elif action == "move":
                    if not os.path.exists(wma_destination):
                        os.makedirs(wma_destination)
                    destination_file = os.path.join(wma_destination, os.path.basename(input_file))
                    shutil.move(input_file, destination_file)
                    logging.info(f"Moved original {input_format.upper()} file: {input_file} to {destination_file}")

                    # Log original destinations of the audio files in a text file
                    with open(os.path.join(wma_destination, "original_locations.txt"), "a") as f:
                        f.write(f"{os.path.abspath(input_file)}\n")
            else:
                if result == "FileExists":
                    logging.warning(f"Output file already exists: {output_file}. Skipping conversion.")
                else:
                    logging.error(f"Failed to convert {input_file}: {result}")

    # Log the end of the script
    logging.info("Script finished")

if __name__ == '__main__':
    # Set up the argument parser and parse the command-line arguments
    parser = argparse.ArgumentParser(description='Convert audio files in a given folder and its subfolders.')
    parser.add_argument('-f', '--folder-path', required=True, type=str, help='Path to the folder containing audio files')
    parser.add_argument('-i', '--input-format', default='wma', choices=['wma', 'flac', 'wav', 'm4a', 'ogg'], type=str, help='Input format for audio files (default: wma)')
    parser.add_argument('-o', '--output-format', default='mp3', choices=['mp3', 'flac', 'wav', 'm4a', 'ogg'], type=str, help='Output format for converted files (default: mp3)')
    parser.add_argument('-l', '--log-file', default='audio_conversion.log', type=str, help='Log file path (default: audio_conversion.log)')
    parser.add_argument('-a', '--action', choices=['none', 'remove', 'move'], default='none', help='Action for original audio files after conversion: none (default), remove, or move')
    parser.add_argument('-w', '--wma-destination', default='audio_backup', type=str, help='Destination folder for moved audio files (default: audio_backup)')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing output files if they already exist')
    parser.add_argument('--log-level', default='info', type=str, help='Logging level: debug, info (default), warning, error, or critical')
    parser.add_argument('-q', '--audio-quality', default='high', choices=['low', 'medium', 'high'], type=str, help='Audio quality for output files (default: high)')

    args = parser.parse_args()
    
    # Call the main function with the parsed arguments
    main(args)

