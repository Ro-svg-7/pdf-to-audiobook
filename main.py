import tkinter as tk
from tkinter import filedialog, ttk
from PyPDF2 import PdfReader
import pyttsx3

root = tk.Tk()
root.title("PDF to AudioBook")
root.geometry("600x400")
root.configure(bg="black")

selected_file = tk.StringVar()
status_text = tk.StringVar()

selected_file.set("No PDF selected")
status_text.set("Waiting for file...")

def upload_pdf():
    filepath = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf")]
    )

    if filepath:
        selected_file.set(filepath)
        status_text.set("PDF upload successful")

def convert_to_audio():
    if selected_file.get() == "No PDF selected":
        status_text.set("Please upload a PDF file")
        return
    status_text.set("Converting PDF to audiobook...")

    text = extract_text()
    
    status_text.set("Converting to Audiobook...")

    engine = pyttsx3.init()

    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1)

    output_file = "audiobook.mp3"

    engine.save_to_file(text, output_file)

    engine.runAndWait()

    status_text.set("Audiobook created successfully!")

def extract_text():
    pdf_path = selected_file.get()

    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        number_of_pages = len(reader.pages)
        full_text = ""

        for i in range(number_of_pages):
            page = reader.pages[i]
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    print(full_text)
    return full_text

title_label = tk.Label(
    root,
    text="PDF to Audiobook Converter",
    font=("Arial", 22, "bold"),
    bg="#1e1e1e",
    fg="white"
)

title_label.pack(pady=20)

file_label = tk.Label(
    root,
    text="Upload PDF",
    font=("Arial", 12),
    bg="black",
    fg="white",
    padx=20,
    pady=10
)
file_label.pack(pady=10)

upload_button = tk.Button(
    root,
    text="Upload Button",
    font=("Arial", 12),
    bg="#4CAF50",
    fg="white",
    padx=20,
    pady=10,
    command=upload_pdf
)
upload_button.pack(pady=10)

convert_button = tk.Button(
    root,
    text="Convert to Audiobook",
    font=("Arial", 12),
    bg="#2196F3",
    fg="white",
    padx=20,
    pady=10,
    command=convert_to_audio
)
convert_button.pack(pady=10)

progress = ttk.Progressbar(
    root,
    orient="horizontal",
    length=400,
    mode="determinate"
)

progress.pack(pady=20)

status_label = tk.Label(
    root,
    textvariable=status_text,
    font=("Arial", 10),
    bg="#1e1e1e",
    fg="#aaaaaa"
)

status_label.pack(pady=10)

root.mainloop()