#you can interact with the convert script through this gradio interface gui if you prefer that 
import gradio as gr
import subprocess
import os

def run_script(ebook_file, target_voice_file):
    python_executable = "python3" if os.name != "nt" else "python"
    command = [python_executable, "styletts_to_ebook.py", ebook_file]
    if target_voice_file:
        command.append(target_voice_file)

    # Open a subprocess and redirect its output to a pipe
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Create a string to capture the output
    output_str = ""

    # Read the output line by line and append to the string
    while process.poll() is None:
        line = process.stdout.readline()
        output_str += line
        if line:
            print(line)  # Print each line to the console

    # Capture any remaining output
    remaining_output = process.communicate()[0]
    output_str += remaining_output

    return output_str

def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        file_path = os.path.join("uploads", uploaded_file.name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            file.write(uploaded_file.read())
        return file_path
    return None

def interface_fn(ebook_file, target_voice_file):
    ebook_file_path = ebook_file.name  # Pass the file object directly
    target_voice_path = target_voice_file.name if target_voice_file is not None else None

    if not ebook_file_path:
        return "Please upload an eBook file."

    return run_script(ebook_file_path, target_voice_path)

interface = gr.Interface(
    fn=interface_fn,
    inputs=[
        gr.File(label="Upload eBook File"),
        gr.File(label="Upload Target Voice File (Optional)"),  # Remove optional=True
    ],
    outputs="text",
    title="eBook to Audiobook Converter",
    description="Convert eBooks to Audiobooks using styletts_to_ebook.py"
)

if __name__ == "__main__":
    interface.launch()
