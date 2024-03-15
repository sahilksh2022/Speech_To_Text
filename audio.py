import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import assemblyai as aai
from fpdf import FPDF
import os

# Set your AssemblyAI API key
aai.settings.api_key = "2e6fbc59dbbe49d1998c05f98e40d07d"

class TranscribeThread(threading.Thread):
    def __init__(self, audio_file_path):
        super().__init__()
        self.audio_file_path = audio_file_path
        self.transcript_text = None
        self.transcription_complete = False

    def run(self):
        try:
            transcriber = aai.Transcriber()
            self.transcript_text = transcriber.transcribe(self.audio_file_path).text
        except Exception as e:
            print("Transcription error:", e)
        finally:
            self.transcription_complete = True

def transcribe_audio(audio_file_path, progress_label):
    progress_label.config(text="Transcribing...")
    transcribe_thread = TranscribeThread(audio_file_path)
    transcribe_thread.start()
    while not transcribe_thread.transcription_complete:
        progress_label.update()
        time.sleep(0.5)
    if transcribe_thread.transcript_text:
        progress_label.config(text="Transcription Complete")
        return transcribe_thread.transcript_text
    else:
        progress_label.config(text="Transcription Failed")

def create_pdf(transcript_text, output_filename="transcript.pdf"):
    try:
        # Create a PDF object
        pdf = FPDF()
        pdf.add_page()

        # Set font for the PDF
        pdf.set_font("Arial", size=12)

        # Set maximum width for the text in the PDF
        max_width = 180

        # Split the transcript text into lines
        lines = transcript_text.split('\n')

        # Add each line of the transcript to the PDF
        for line in lines:
            words = line.split(' ')
            current_line = ''
            for word in words:
                if pdf.get_string_width(current_line + ' ' + word) <= max_width:
                    current_line += ' ' + word
                else:
                    pdf.cell(200, 10, txt=current_line.strip(), ln=True)
                    current_line = word
            # Add the last line
            pdf.cell(200, 10, txt=current_line.strip(), ln=True)

        # Save the PDF to a file
        pdf.output(output_filename)
        print("PDF created successfully:", output_filename)
        return output_filename
    except Exception as e:
        print("PDF creation error:", e)

def transcribe_and_create_pdf(progress_label):
    audio_file_path = filedialog.askopenfilename(title="Select Audio File")
    if audio_file_path:
        transcript_text = transcribe_audio(audio_file_path, progress_label)
        if transcript_text:
            output_filename = audio_file_path.split("/")[-1].split(".")[0] + ".pdf"
            pdf_path = create_pdf(transcript_text, output_filename)
            if pdf_path:
                messagebox.showinfo("PDF Saved", f"PDF saved as {output_filename}")
                open_pdf = messagebox.askquestion("Open PDF", "Do you want to open the saved PDF?")
                if open_pdf == "yes":
                    os.system("start " + pdf_path)

# Create the main window
root = tk.Tk()
root.title("Audio Transcription and PDF Creation")

# Create a button to transcribe and create PDF
transcribe_button = tk.Button(root, text="Transcribe and Create PDF", command=lambda: transcribe_and_create_pdf(progress_label))
transcribe_button.pack(pady=20)

# Create a label to show progress
progress_label = tk.Label(root, text="")
progress_label.pack()

# Run the Tkinter event loop
root.mainloop()
