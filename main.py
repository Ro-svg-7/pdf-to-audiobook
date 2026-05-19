import os
import tkinter as tk
from tkinter import filedialog, ttk
from PyPDF2 import PdfReader
import pyttsx3

root = tk.Tk()
root.title("PDF to AudioBook")
root.geometry("700x500")
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

            progress["value"] = ((i+1) / number_of_pages) * 100
            root.update_idletasks()

    return full_text

def convert_to_audio():
    pdf_path = selected_file.get()
    pdf_name = os.path.basename(pdf_path)
    pdf_name = os.path.splitext(pdf_name)[0]

    if selected_file.get() == "No PDF selected":
        status_text.set("Please upload a PDF file")
        return
    status_text.set("Converting PDF to audiobook...")

    text = extract_text()
    
    status_text.set("Converting to Audiobook...")

    engine = pyttsx3.init()

    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1)

    output_file = filedialog.asksaveasfilename(
        defaultextension=".mp3",
        initialfile=f"{pdf_name}_audiobook.mp3",
        filetypes=[("MP3 Files", "*mp3")]
    )

    if output_file:
        engine.save_to_file(text, output_file)

        engine.runAndWait()

        status_text.set("Audiobook created successfully!")
    else:
        return
    
title_label = tk.Label(
    root,
    text="PDF to Audiobook Converter",
    font=("Arial", 24, "bold"),
    bg="#1e1e1e",
    fg="white"
)

title_label.pack(pady=25)

file_label = tk.Label(
    root,
    textvariable=selected_file,
    font=("Arial", 10),
    bg="black",
    fg="#bbbbbb",
    wraplength=500
)
file_label.pack(pady=10)

upload_button = tk.Button(
    root,
    text="Upload Button",
    font=("Arial", 12,"bold"),
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    padx=25,
    pady=12,
    command=upload_pdf
)
upload_button.pack(pady=15)

convert_button = tk.Button(
    root,
    text="Convert to Audiobook",
    font=("Arial", 12, "bold"),
    bg="#2196F3",
    fg="white",
    activebackground="#1976D2",
    relief="flat",
    padx=25,
    pady=12,
    command=convert_to_audio
)
convert_button.pack(pady=10)

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Custom.Horizontal.TProgressbar",
    troughcolor="#2b2b2b",
    background="#2196F3",
    bordercolor = "#2b2b2b",
    lightcolor="#2196F3",
    darkcolor="#2196F3"
)

progress = ttk.Progressbar(
    root,
    style="Custom.Horizontal.TProgressbar",
    orient="horizontal",
    length=450,
    mode="determinate"
)

progress.pack(pady=30)

status_label = tk.Label(
    root,
    textvariable=status_text,
    font=("Arial", 11),
    bg="#1e1e1e",
    fg="#aaaaaa"
)

status_label.pack(pady=10)

root.mainloop()