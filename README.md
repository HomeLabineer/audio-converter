# Audio Converter

This is a command-line tool for converting audio files from one format to another. The tool supports batch processing of audio files in a given folder and its subfolders.

---

## Features

- Batch processing of audio files in a folder and its subfolders
- Supports multiple input and output formats (mp3, wma, flac, m4a, ogg, aac, alac, opus, ape, aiff)
- Selectable audio quality for output files (low, medium, high)
- Optional actions for original audio files after conversion (none, remove, or move)
- Customizable logging levels and log file path
- Status bar whilst running:
```bash
Converting:  37%|██████████████████████████████████████▍                                                                  | 787/2153 [07:51<13:23,  1.70it/s]
```

---

## Requirements

- Python 3.x
- ffmpy
- tqdm
- ffmpeg

---

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

---

## Usage

```bash
usage: audio_converter.py [-h] -f FOLDER_PATH [-i {wma,flac,wav,m4a,ogg,aac,alac,opus,ape,aiff,all} [{wma,flac,wav,m4a,ogg,aac,alac,opus,ape,aiff,all} ...]] [-o {mp3,flac,wav,m4a,aac,alac,opus,ape,aiff}]
                           [-l LOG_FILE] [-a {none,remove,move}] [-w WMA_DESTINATION] [--overwrite] [--log-level LOG_LEVEL]
                           [-q {low,medium,high}]

Convert audio files in a given folder and its subfolders.

optional arguments:
  -h, --help            show this help message and exit
  -f FOLDER_PATH, --folder-path FOLDER_PATH
                        Path to the folder containing audio files
  -i {wma,flac,wav,m4a,ogg,aac,alac,opus,ape,aiff,all} [{wma,flac,wav,m4a,ogg,aac,alac,opus,ape,aiff,all} ...], --input-format {wma,flac,wav,m4a,ogg,aac,alac,opus,ape,aiff,all} [{wma,flac,wav,m4a,ogg,aac,alac,opus,ape,aiff,all} ...]
                        Input format for audio files (default: wma)
  -o {mp3,flac,wav,m4a,aac,alac,opus,ape,aiff}, --output-format {mp3,flac,wav,m4a,aac,alac,opus,ape,aiff}
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

---

### Additional Usage Insight:

1. The purpose of `--action` is to allow you to choose to leave the original file where it is, move it to a safe location so you can review/test the conversions before deleting the original OR you can have the script delete the original which is not recommended.  However, if you have a NAS with a network recycle bin, this option may not be so scary.

2. `--overwrite` is intended to be a check that a version of the same named file doesn't already exist with the new format's extension.  I.E. you are converting all WMA formats to MP3:

  `Some Artist - Some Album - Some Track Number - Some Song Title.wma` and `Some Artist - Some Album - Some Track Number - Some Song Title.mp3`

  If you don't provide the `--overwrite` flag, by default it would skip converting this which is nice because it saves compute time.  But maybe you want to overwrite for some reason.  Maybe you are reducing quality, increasing quality (this is a catch 22 because if you convert a low quality file to a high quality, it's still effectively low quality) or maybe you have an album with various quality types, MP3 @ 60k, 128k, 192k and 320k.  And you want them all the same for whatever reason.  

3. By default, the ThreadPoolExecutor uses the number of CPUs on the machine as the number of threads in the pool. You can explicitly set the number of threads by passing the `--max_workers` parameter.  If you have 8 cores, try 4 or 6 to prevent maxing out all cores.  Leaving this setting on default can max out all CPU cores easily as ffmpeg wants to work as quickly as possible. 

---

## Examples

1. Convert all WMA files in a folder to MP3 files with high quality:

`python audio_converter.py -f /path/to/your/folder`

2. Convert all FLAC files in a folder to M4A files with medium quality and remove the original files after conversion:

`python audio_converter.py -f /path/to/your/folder -i flac -o m4a -q medium -a remove`

3. Convert multiple types:

`python3 audio_converter.py --folder-path /path/to/folder --input-format wma flac m4a --output-format mp3`

---

## Contributing

Thank you for your interest in contributing to my Audio Converter! We appreciate your help in making this project better. Here are some guidelines to help ensure a smooth contribution process:

If you want to contribute and support my work, you can do so at the following:

<a href="https://github.com/sponsors/homelabineer">
  <img src="https://img.shields.io/badge/Sponsor_on-GitHub-green?logo=github&style=flat-square" alt="GitHub Sponsors" />
</a>
<a href="https://www.patreon.com/homelabineer">
  <img src="https://img.shields.io/badge/Support_on-Patreon-orange?logo=patreon&style=flat-square" alt="Patreon" />
</a>
<a href="https://paypal.me/homelabineer?country.x=US&locale.x=en_US">
  <img src="https://img.shields.io/badge/Donate-PayPal-green.svg?style=flat-square&logo=paypal" alt="PayPal" />
</a>

---

### Reporting issues

If you encounter any issues with the project, please create a new issue on the [Issues](https://github.com/HomeLabineer/audio-converter/issues) page. When reporting an issue, please provide the following information:

- A clear and concise description of the issue
- Steps to reproduce the issue
- Expected and actual behavior
- Any relevant logs or error messages

---

### Submitting pull requests

If you would like to submit a pull request, please follow these steps:

1. Fork the repository and create your own branch with a descriptive name, such as `feature/my-new-feature` or `bugfix/my-bugfix`.

2. Make your changes in the new branch, ensuring that you follow the project's coding standards and best practices.

3. Write tests, if applicable, to cover any new functionality or to reproduce and fix any reported issues.

4. Update the documentation, including README and inline comments, to reflect your changes.

5. Before submitting your pull request, make sure your branch is up-to-date with the main branch and that your code passes all tests and linter checks.

6. Create a pull request with a clear and concise description of your changes. In your pull request message, please include any relevant information, such as the issue being addressed, new features added, or bugfixes applied.

---

## Credits

This project was developed using various programming tools, including the ChatGPT-4 language model. ChatGPT-4 was used to assist with tasks such as generating code snippets, providing suggestions for code improvements, and writing documentation such as this README.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.