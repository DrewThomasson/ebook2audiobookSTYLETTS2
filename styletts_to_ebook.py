import os
import subprocess
import re
from pydub import AudioSegment
def is_folder_empty(folder_path):
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # List directory contents
        if not os.listdir(folder_path):
            return True  # The folder is empty
        else:
            return False  # The folder is not empty
    else:
        print(f"The path {folder_path} is not a valid folder.")
        return None  # The path is not a valid folder

def wipe_folder(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return

    # Iterate through all items in the folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try:
            # If it's a file, remove it
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"Removed file: {item_path}")
            # If it's a directory, you can decide whether to delete it or not
            elif os.path.isdir(item_path):
                print(f"Found directory, not removing: {item_path}")
                # Optionally, you can call wipe_folder recursively if you want to delete subdirectories:
                # wipe_folder(item_path)
        except Exception as e:
            print(f"Failed to remove {item_path}. Reason: {e}")

# Example usage
# folder_to_wipe = 'path_to_your_folder'
# wipe_folder(folder_to_wipe)


# Example usage
# folder_to_wipe = 'Working_files/temp_ebook'  # Replace with the path to your folder
# wipe_folder(folder_to_wipe)


def create_m4b_from_chapters(input_dir, ebook_file, output_dir):
    # Function to sort chapters based on their numeric order
    def sort_key(chapter_file):
        numbers = re.findall(r'\d+', chapter_file)
        return int(numbers[0]) if numbers else 0

    # Extract metadata and cover image from the eBook file
    def extract_metadata_and_cover(ebook_path):
        try:
            cover_path = ebook_path.rsplit('.', 1)[0] + '.jpg'
            subprocess.run(['ebook-meta', ebook_path, '--get-cover', cover_path], check=True)
            if os.path.exists(cover_path):
                return cover_path
        except Exception as e:
            print(f"Error extracting eBook metadata or cover: {e}")
        return None

    # Combine WAV files into a single file
    def combine_wav_files(chapter_files, output_path):
        combined = AudioSegment.empty()
        for chapter_file in chapter_files:
            combined += AudioSegment.from_wav(chapter_file)
        combined.export(output_path, format='wav')

    # Function to generate metadata for M4B chapters
    def generate_ffmpeg_metadata(chapter_files, metadata_file):
        with open(metadata_file, 'w') as file:
            file.write(';FFMETADATA1\n')
            start_time = 0
            for index, chapter_file in enumerate(chapter_files):
                duration_ms = len(AudioSegment.from_wav(chapter_file))
                file.write(f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={start_time}\n')
                file.write(f'END={start_time + duration_ms}\ntitle=Chapter {index + 1}\n')
                start_time += duration_ms

    # Generate the final M4B file using ffmpeg
    def create_m4b(combined_wav, metadata_file, cover_image, output_m4b):
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_m4b), exist_ok=True)
        
        ffmpeg_cmd = ['ffmpeg', '-i', combined_wav, '-i', metadata_file]
        if cover_image:
            ffmpeg_cmd += ['-i', cover_image, '-map', '0:a', '-map', '2:v']
        else:
            ffmpeg_cmd += ['-map', '0:a']
        
        ffmpeg_cmd += ['-map_metadata', '1', '-c:a', 'aac', '-b:a', '192k']
        if cover_image:
            ffmpeg_cmd += ['-c:v', 'png', '-disposition:v', 'attached_pic']
        ffmpeg_cmd += [output_m4b]

        subprocess.run(ffmpeg_cmd, check=True)



    # Main logic
    chapter_files = sorted([os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.wav')], key=sort_key)
    temp_combined_wav = os.path.join('/tmp', 'combined.wav')
    metadata_file = os.path.join('/tmp', 'metadata.txt')
    cover_image = extract_metadata_and_cover(ebook_file)
    output_m4b = os.path.join(output_dir, os.path.splitext(os.path.basename(ebook_file))[0] + '.m4b')

    combine_wav_files(chapter_files, temp_combined_wav)
    generate_ffmpeg_metadata(chapter_files, metadata_file)
    create_m4b(temp_combined_wav, metadata_file, cover_image, output_m4b)

    # Cleanup
    if os.path.exists(temp_combined_wav):
        os.remove(temp_combined_wav)
    if os.path.exists(metadata_file):
        os.remove(metadata_file)
    if cover_image and os.path.exists(cover_image):
        os.remove(cover_image)

# Example usage
# create_m4b_from_chapters('path_to_chapter_wavs', 'path_to_ebook_file', 'path_to_output_dir')






#this code right here isnt the book grabbing thing but its before to refrence in ordero to create the sepecial chapter labeled book thing with calibre idk some systems cant seem to get it so just in case but the next bit of code after this is the book grabbing code with booknlp 
import os
import subprocess
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
import csv
import nltk

# Only run the main script if Value is True
def create_chapter_labeled_book(ebook_file_path):
    # Function to ensure the existence of a directory
    def ensure_directory(directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Created directory: {directory_path}")

    ensure_directory('Working_files/Book')

    def convert_to_epub(input_path, output_path):
        # Convert the ebook to EPUB format using Calibre's ebook-convert
        try:
            subprocess.run(['ebook-convert', input_path, output_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while converting the eBook: {e}")
            return False
        return True

    def save_chapters_as_text(epub_path):
        # Create the directory if it doesn't exist
        directory = "Working_files/temp_ebook"
        ensure_directory(directory)

        # Open the EPUB file
        book = epub.read_epub(epub_path)

        previous_chapter_text = ''
        previous_filename = ''
        chapter_counter = 0

        # Iterate through the items in the EPUB file
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # Use BeautifulSoup to parse HTML content
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                text = soup.get_text()

                # Check if the text is not empty
                if text.strip():
                    if len(text) < 2300 and previous_filename:
                        # Append text to the previous chapter if it's short
                        with open(previous_filename, 'a', encoding='utf-8') as file:
                            file.write('\n' + text)
                    else:
                        # Create a new chapter file and increment the counter
                        previous_filename = os.path.join(directory, f"chapter_{chapter_counter}.txt")
                        chapter_counter += 1
                        with open(previous_filename, 'w', encoding='utf-8') as file:
                            file.write(text)
                            print(f"Saved chapter: {previous_filename}")

    # Example usage
    input_ebook = ebook_file_path  # Replace with your eBook file path
    output_epub = 'Working_files/temp.epub'

    if os.path.exists(output_epub):
        os.remove(output_epub)
        print(f"File {output_epub} has been removed.")
    else:
        print(f"The file {output_epub} does not exist.")

    if convert_to_epub(input_ebook, output_epub):
        save_chapters_as_text(output_epub)

    # Download the necessary NLTK data (if not already present)
    nltk.download('punkt')
    """
    def process_chapter_files(folder_path, output_csv):
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write the header row
            writer.writerow(['Text', 'Start Location', 'End Location', 'Is Quote', 'Speaker', 'Chapter'])

            # Process each chapter file
            chapter_files = sorted(os.listdir(folder_path), key=lambda x: int(x.split('_')[1].split('.')[0]))
            for filename in chapter_files:
                if filename.startswith('chapter_') and filename.endswith('.txt'):
                    chapter_number = int(filename.split('_')[1].split('.')[0])
                    file_path = os.path.join(folder_path, filename)

                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            text = file.read()
                            sentences = nltk.tokenize.sent_tokenize(text)
                            for sentence in sentences:
                                start_location = text.find(sentence)
                                end_location = start_location + len(sentence)
                                writer.writerow([sentence, start_location, end_location, 'True', 'Narrator', chapter_number])
                    except Exception as e:
                        print(f"Error processing file {filename}: {e}")
    """

    
    def process_chapter_files(folder_path, output_csv):
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write the header row
            writer.writerow(['Text', 'Start Location', 'End Location', 'Is Quote', 'Speaker', 'Chapter'])

            # Process each chapter file
            chapter_files = sorted(os.listdir(folder_path), key=lambda x: int(x.split('_')[1].split('.')[0]))
            for filename in chapter_files:
                if filename.startswith('chapter_') and filename.endswith('.txt'):
                    chapter_number = int(filename.split('_')[1].split('.')[0])
                    file_path = os.path.join(folder_path, filename)

                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            text = file.read()
                            # Insert "NEWCHAPTERABC" at the beginning of each chapter's text
                            if text:
                                text = "NEWCHAPTERABC" + text
                            sentences = nltk.tokenize.sent_tokenize(text)
                            for sentence in sentences:
                                start_location = text.find(sentence)
                                end_location = start_location + len(sentence)
                                writer.writerow([sentence, start_location, end_location, 'True', 'Narrator', chapter_number])
                    except Exception as e:
                        print(f"Error processing file {filename}: {e}")

    # Example usage
    folder_path = "Working_files/temp_ebook"  # Replace with your folder path
    output_csv = 'Working_files/Book/Other_book.csv'
    process_chapter_files(folder_path, output_csv)

    def sort_key(filename):
        """Extract chapter number for sorting."""
        match = re.search(r'chapter_(\d+)\.txt', filename)
        return int(match.group(1)) if match else 0

    def combine_chapters(input_folder, output_file):
        # Create the output folder if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # List all txt files and sort them by chapter number
        files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
        sorted_files = sorted(files, key=sort_key)

        with open(output_file, 'w') as outfile:
            for i, filename in enumerate(sorted_files):
                with open(os.path.join(input_folder, filename), 'r') as infile:
                    outfile.write(infile.read())
                    # Add the marker unless it's the last file
                    if i < len(sorted_files) - 1:
                        outfile.write("\nNEWCHAPTERABC\n")

    # Paths
    input_folder = 'Working_files/temp_ebook'
    output_file = 'Working_files/Book/Chapter_Book.txt'

    # Combine the chapters
    combine_chapters(input_folder, output_file)

    ensure_directory('Working_files/Book')

#create_chapter_labeled_book()






import os
import subprocess
from styletts2 import tts
import sys

# Check if Calibre's ebook-convert tool is installed
def calibre_installed():
    try:
        subprocess.run(['ebook-convert', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        print("Calibre is not installed. Please install Calibre for this functionality.")
        return False

# Convert eBook to text using Calibre
def convert_ebook_to_text(ebook_path):
    output_path = ebook_path.rsplit('.', 1)[0] + '.txt'
    subprocess.run(['ebook-convert', ebook_path, output_path])
    return output_path

# Split eBook into chapters
def split_ebook_into_chapters(text_path):
    chapters_dir = "chapters"
    os.makedirs(chapters_dir, exist_ok=True)
    with open(text_path, 'r', encoding='utf-8') as file:
        text = file.read()
    chapters = text.split("Chapter")  # Adjust based on your chapter delimiter
    for i, chapter in enumerate(chapters):
        with open(os.path.join(chapters_dir, f"chapter_{i}.txt"), 'w', encoding='utf-8') as chapter_file:
            chapter_file.write(chapter)
    return chapters_dir

# Process text files (optional)
def process_text_files(chapters_dir):
    for filename in os.listdir(chapters_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(chapters_dir, filename), 'r', encoding='utf-8') as file:
                lines = [line for line in file if line.strip()]
            with open(os.path.join(chapters_dir, filename), 'w', encoding='utf-8') as file:
                file.writelines(lines)

# Convert chapters to audio using StyleTTS2
def convert_chapters_to_audio(chapters_dir, output_audio_dir, target_voice_path=None):
    my_tts = tts.StyleTTS2()

    if not os.path.exists(output_audio_dir):
        os.makedirs(output_audio_dir)

    for chapter_file in sorted(os.listdir(chapters_dir)):
        if chapter_file.endswith('.txt'):
            chapter_path = os.path.join(chapters_dir, chapter_file)
            output_file_path = os.path.join(output_audio_dir, chapter_file.replace('.txt', '.wav'))
            with open(chapter_path, 'r', encoding='utf-8') as file:
                chapter_text = file.read()
            if target_voice_path:
                my_tts.inference(chapter_text, target_voice_path=target_voice_path, output_wav_file=output_file_path)
            else:
                my_tts.inference(chapter_text, output_wav_file=output_file_path)
            print(f"Converted {chapter_file} to audio.")


# Main execution flow
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <ebook_file_path> [target_voice_file_path]")
        sys.exit(1)

    ebook_file_path = sys.argv[1]
    target_voice = sys.argv[2] if len(sys.argv) > 2 else None

    if not calibre_installed():
        sys.exit(1)

    create_chapter_labeled_book(ebook_file_path)
    #text_file_path = convert_ebook_to_text(ebook_file_path)
    #chapters_directory = split_ebook_into_chapters(text_file_path)
    chapters_directory = "Working_files/temp_ebook"
    #process_text_files(chapters_directory)
    output_audio_directory = 'Chapter_wav_files'
    if is_folder_empty == False:
        wipe_folder(output_audio_directory)
        wipe_folder(chapters_directory)
    audiobook_output_path = "Audiobooks"
    print(f"{chapters_directory}||||{output_audio_directory}|||||{target_voice}")
    convert_chapters_to_audio(chapters_directory, output_audio_directory, target_voice)
    create_m4b_from_chapters(output_audio_directory, ebook_file_path, audiobook_output_path)
