@echo off
REM Check for Administrator privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Administrator privileges confirmed.
) else (
    echo This script requires Administrator privileges.
    pause
    exit
)

REM Install Chocolatey
echo Installing Chocolatey...
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"

REM Install Python, Git, and other dependencies via Chocolatey
echo Installing Python, Git, Calibre, and FFMPEG...
choco install python --version=3.10 -y
choco install git -y
choco install pip -y
choco install calibre -y
choco install ffmpeg -y


REM Install Python packages
echo Installing Python packages...
pip install styletts2 pydub nltk beautifulsoup4 ebooklib

REM Clone the GitHub repository
echo Cloning the GitHub repository...
git clone https://github.com/DrewThomasson/ebook2audiobookSTYLETTS2.git

REM Instructions for running the Python script
echo.
echo Installation complete. To run the Python program, navigate to the ebook2audiobookSTYLETTS2 directory and use:
echo python styletts_to_ebook.py ^<path_to_ebook_file^>
echo or
echo python styletts_to_ebook.py ^<path_to_ebook_file^> ^<path_to_voice_file^>
echo.

echo  running test miniStory file…
cd ebook2audiobookSTYLETTS2 
python styletts_to_ebook.py demo_mini_story_chapters_Drew.epub

echo Complete! Check folder.
pause