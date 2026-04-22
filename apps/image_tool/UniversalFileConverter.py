import os
import subprocess
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image

root = Tk()
root.title("Universal File Converter")
root.geometry("700x600")
root.configure(bg="#1e293b")

selected_file = ""

def select_file():
    global selected_file
    selected_file = filedialog.askopenfilename()
    file_label.config(text=selected_file)

def convert_image():
    if not selected_file:
        messagebox.showerror("Error", "Select image first")
        return

    try:
        img = Image.open(selected_file)

        width = width_entry.get()
        height = height_entry.get()
        quality = int(quality_entry.get())

        if width and height:
            img = img.resize((int(width), int(height)))

        format_selected = format_var.get()

        save_path = filedialog.asksaveasfilename(
            defaultextension="." + format_selected,
            filetypes=[(format_selected.upper(), "*." + format_selected)]
        )

        img.save(save_path, format_selected.upper(), quality=quality)
        messagebox.showinfo("Success", "Image converted!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def convert_ffmpeg():
    if not selected_file:
        messagebox.showerror("Error", "Select file first")
        return

    format_selected = format_var.get()

    save_path = filedialog.asksaveasfilename(
        defaultextension="." + format_selected,
        filetypes=[(format_selected.upper(), "*." + format_selected)]
    )

    command = ["ffmpeg", "-i", selected_file, save_path]

    try:
        subprocess.run(command)
        messagebox.showinfo("Success", "Conversion finished!")
    except:
        messagebox.showerror("Error", "FFmpeg not found!")


def convert_libreoffice():
    if not selected_file:
        messagebox.showerror("Error", "Select file first")
        return

    format_selected = format_var.get()
    output_dir = os.path.dirname(selected_file)

    command = [
        "soffice",
        "--headless",
        "--convert-to",
        format_selected,
        "--outdir",
        output_dir,
        selected_file
    ]

    try:
        subprocess.run(command)
        messagebox.showinfo("Success", "File converted in same folder!")
    except:
        messagebox.showerror("Error", "LibreOffice not found!")


Label(root, text="Universal File Converter PRO",
      bg="#1e293b", fg="white", font=("Arial", 18)).pack(pady=20)

Button(root, text="Select File", command=select_file,
       bg="#3b82f6", fg="white").pack(pady=10)

file_label = Label(root, text="No file selected",
                   bg="#1e293b", fg="lightgray")
file_label.pack()

Label(root, text="Image Resize (optional)",
      bg="#1e293b", fg="white").pack(pady=10)

width_entry = Entry(root)
width_entry.pack()
width_entry.insert(0, "")

height_entry = Entry(root)
height_entry.pack()
height_entry.insert(0, "")

Label(root, text="Image Quality (1-100)",
      bg="#1e293b", fg="white").pack()

quality_entry = Entry(root)
quality_entry.pack()
quality_entry.insert(0, "90")

format_var = StringVar()
format_var.set("jpg")

formats = [
    # Images
    "jpg", "png", "webp", "bmp", "tiff",
    # Audio
    "mp3", "wav", "ogg", "flac", "aac",
    # Video
    "mp4", "avi", "mkv", "mov", "wmv",
    # Documents
    "pdf", "docx", "txt", "rtf", "odt",
    # Tables
    "xlsx", "csv", "ods",
    # Presentations
    "pptx"
]

OptionMenu(root, format_var, *formats).pack(pady=10)

Button(root, text="Convert Image (Pillow)",
       command=convert_image,
       bg="#10b981", fg="white").pack(pady=5)

Button(root, text="Convert Audio/Video (FFmpeg)",
       command=convert_ffmpeg,
       bg="#f59e0b", fg="white").pack(pady=5)

Button(root, text="Convert Documents (LibreOffice)",
       command=convert_libreoffice,
       bg="#ef4444", fg="white").pack(pady=5)

root.mainloop()
