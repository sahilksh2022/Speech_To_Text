import os
import sys
import time
import azure.cognitiveservices.speech as speechsdk
import tkinter as tk
from tkinter import filedialog, messagebox

# Colors for colored output
BLUE = '\033[94m'
RED = '\033[91m'
GREEN = '\033[92m'
ENDC = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def select_input_file():
    input_file_path = filedialog.askopenfilename(title="Select Input File")
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, input_file_path)

def start_recognition():
    API_KEY = api_key_entry.get()
    REGION = region_entry.get()
    INPUT_FILE_PATH = input_file_entry.get()
    OUTPUT_FILE_PATH = output_file_entry.get()
    LANGUAGE = language_entry.get()

    if not all([API_KEY, REGION, INPUT_FILE_PATH, OUTPUT_FILE_PATH, LANGUAGE]):
        messagebox.showerror("Error", "Please fill in all fields")
        return

    try:
        speech_config = speechsdk.SpeechConfig(
            subscription=API_KEY,
            region=REGION,
            speech_recognition_language=LANGUAGE
        )
        audio_config = speechsdk.AudioConfig(filename=INPUT_FILE_PATH)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        recognition_status.set("Recognizing...")
        root.update()

        done = False
        all_results = []

        def stop_cb(evt):
            speech_recognizer.stop_continuous_recognition()
            nonlocal done
            done = True

            if evt.result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = evt.result.cancellation_details
                cancellation_reason = cancellation_details.reason
                if cancellation_reason == speechsdk.CancellationReason.Error:
                    recognition_status.set("Error: " + cancellation_details.error_details)
                elif cancellation_reason == speechsdk.CancellationReason.CancelledByUser:
                    recognition_status.set("Cancelled by user")
                elif cancellation_reason == speechsdk.CancellationReason.EndOfStream:
                    recognition_status.set("Success")

        def handle_final_result(evt):
            nonlocal all_results
            all_results.append(evt.result.text)

        speech_recognizer.recognized.connect(handle_final_result)
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        speech_recognizer.start_continuous_recognition()
        while not done:
            root.update()
            time.sleep(0.1)

        if all_results:
            with open(OUTPUT_FILE_PATH, "w", encoding="utf-8") as output:
                for result in all_results:
                    output.write(result + "\n")
            recognition_status.set("Text saved to file")
            open_pdf = messagebox.askquestion("Open PDF", "Do you want to open the saved PDF?")
            if open_pdf == "yes":
                open_generated_file(OUTPUT_FILE_PATH)
                    #os.system("start " + pdf_path)
                   
           

    except Exception as e:
        recognition_status.set("Error: " + str(e))

def open_generated_file(output_file_path):
    if os.path.isfile(output_file_path):
        os.startfile(output_file_path)
        messagebox.showinfo("File Opened", f"The generated file has been opened: {output_file_path}")
    else:
        messagebox.showerror("Error", "Output file not found")

root = tk.Tk()
root.title("Speech to Text Conversion")

api_key_label = tk.Label(root, text="API Key:")
api_key_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
api_key_entry = tk.Entry(root)
api_key_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

region_label = tk.Label(root, text="Region:")
region_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
region_entry = tk.Entry(root)
region_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

input_file_label = tk.Label(root, text="Input File Path:")
input_file_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
input_file_entry = tk.Entry(root)
input_file_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
input_file_button = tk.Button(root, text="Browse", command=select_input_file)
input_file_button.grid(row=2, column=2, padx=5, pady=5)

output_file_label = tk.Label(root, text="Output File Path:")
output_file_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
output_file_entry = tk.Entry(root)
output_file_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

language_label = tk.Label(root, text="Language:")
language_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
language_entry = tk.Entry(root)
language_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

start_button = tk.Button(root, text="Start Recognition", command=start_recognition)
start_button.grid(row=5, column=0, columnspan=3, padx=5, pady=10, sticky="ew")

recognition_status = tk.StringVar()
status_label = tk.Label(root, textvariable=recognition_status)
status_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()
