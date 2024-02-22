# ebook_to_audiobook_styletts

This program uses Calibre for converting eBooks into chapters and StyleTTS2 to transform these chapters into an audiobook. 

It features text-to-speech technology with an optional voice cloning capability if a voice file is provided.
## Demo


https://github.com/DrewThomasson/ebook2audiobookSTYLETTS2/assets/126999465/b55f9fe8-98d1-41ab-a585-3c5b99f9b39f

### Supported ebook File Types: 
.epub, .pdf, .mobi, .txt, .html, .rtf, .chm, .lit, .pdb, .fb2, .odt, .cbr, .cbz, .prc, .lrf, .pml, .snb, .cbc, .rb, and .tcr,
(Best results are from using epub or mobi for auto chapter detection)

### outputs as a m4b with all book metadata and chapters, example output file in an audiobook player app
![Example_of_output_in_audiobook_program](https://github.com/DrewThomasson/VoxNovel/blob/dc5197dff97252fa44c391dc0596902d71278a88/readme_files/example_in_app.jpeg)


## Features

- Converts eBooks to text format using Calibre's `ebook-convert` tool.
- Splits the eBook into chapters for easier processing.
- Utilizes `StyleTTS2` for converting each chapter into an audio file.
- Offers an optional voice cloning feature when provided with a voice file.

## Requirements

- Python 3.10
- `styletts2` Python package
- Calibre (for eBook conversion)
- FFmpeg (for audiobook file creation)
- Optional: Voice file for voice cloning

### Installation Instructions for Dependencies

- Install Python 3.x from [Python.org](https://www.python.org/downloads/).
- Calibre:
  - Ubuntu: `sudo apt-get install -y calibre`
  - macOS: `brew install calibre`
  - Windows(Powershell in Administrator mode): `choco install calibre` 
- FFmpeg:
  - Ubuntu: `sudo apt-get install -y ffmpeg`
  - macOS: `brew install ffmpeg`
  - Windows(Powershell in Administrator mode)s: `choco install ffmpeg` 
- Python packages: 
  ```bash
  pip install styletts2 pydub nltk beautifulsoup4 ebooklib
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


