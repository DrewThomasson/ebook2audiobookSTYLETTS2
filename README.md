# ebook_to_audiobook_styletts
This simple program makes use of Calibre to convert a ebook into chapters and styletts2 to turn that into a audiobook with voice cloning capabilities 


# eBook to Audio Converter

This program converts eBooks into audio format using text-to-speech technology. It can optionally use a specified voice file for voice cloning.

## Features

- Converts eBooks to text format using Calibre's `ebook-convert` tool.
- Splits the eBook into chapters based on a simple delimiter.
- Converts each chapter into an audio file using `StyleTTS2`.
- Optional voice cloning feature if a voice file is provided.

## Requirements

- Python 3.x
- `styletts2` Python package.
- Calibre installed (for eBook conversion).
- Install with sudo apt-get install -y calibre for Ubuntu or brew install calibre for mac
- ffmpeg installed (For audiobook file creation)
- Install with sudo apt-get install -y ffmpeg for Ubuntu or brew install ffmpeg for mac
- Optional: Voice file for voice cloning.

## Installation

1. Install Python 3.x from [Python.org](https://www.python.org/downloads/).
2. Install required Python packages:
   
   ```bash
   pip install styletts2
   pip install pydub
Ensure Calibre is installed on your system for eBook conversion.
Usage

To run the script, navigate to the script's directory in the terminal and use one of the following commands:

Without Voice Cloning:
bash
Copy code
python script.py <path_to_ebook_file>
Replace <path_to_ebook_file> with the path to your eBook file.
With Voice Cloning:
   ```bash
   python styletts_to_ebook.py <path_to_ebook_file> <path_to_voice_file>

#Replace <path_to_ebook_file> with the path to your eBook file and <path_to_voice_file> with the path to the voice file for cloning.
