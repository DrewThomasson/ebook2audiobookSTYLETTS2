# ebook_to_audiobook_styletts

This program uses Calibre for converting eBooks into chapters and StyleTTS2 to transform these chapters into an audiobook. 

It features text-to-speech technology with an optional voice cloning capability if a voice file is provided.


## Features

- Converts eBooks to text format using Calibre's `ebook-convert` tool.
- Splits the eBook into chapters for easier processing.
- Utilizes `StyleTTS2` for converting each chapter into an audio file.
- Offers an optional voice cloning feature when provided with a voice file.

## Requirements

- Python 3.x
- `styletts2` Python package
- Calibre (for eBook conversion)
- FFmpeg (for audiobook file creation)
- Optional: Voice file for voice cloning

### Installation Instructions for Dependencies

- Install Python 3.x from [Python.org](https://www.python.org/downloads/).
- Calibre:
  - Ubuntu: `sudo apt-get install -y calibre`
  - macOS: `brew install calibre`
- FFmpeg:
  - Ubuntu: `sudo apt-get install -y ffmpeg`
  - macOS: `brew install ffmpeg`
- Python packages: 
  ```bash
  pip install styletts2 pydub nltk beautifulsoup4
## Usage

Navigate to the script's directory in the terminal and use one of the following commands:

### Without Voice Cloning:
```bash
python styletts_to_ebook.py <path_to_ebook_file>
```
Replace <path_to_ebook_file> with the path to your eBook file.

### With Voice Cloning:
```bash
python styletts_to_ebook.py <path_to_ebook_file> <path_to_voice_file>
```
Replace <path_to_ebook_file> with the path to your eBook file.

Replace <path_to_voice_file> with the path to the voice file for cloning.


