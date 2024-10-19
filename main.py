import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from PIL import Image, ExifTags, ImageTk
import os
import hashlib
import numpy as np
import image_analysis  # Assuming this is the file containing new features like noise, blurriness, etc.

# Function to extract GPS location from EXIF data
def extract_gps_info(exif_data):
    if 'GPSInfo' in exif_data:
        gps_info = exif_data['GPSInfo']
        
        # Extract latitude and longitude
        lat = gps_info.get(2)  # Latitude in DMS (degrees, minutes, seconds)
        lon = gps_info.get(4)  # Longitude in DMS (degrees, minutes, seconds)

        if lat and lon:
            # Convert DMS to decimal
            latitude = convert_to_degrees(lat)
            longitude = convert_to_degrees(lon)
            return f"Latitude: {latitude:.6f}, Longitude: {longitude:.6f}"
    return "No GPS location found."

# Convert GPS coordinates to degrees
def convert_to_degrees(value):
    d = float(value[0]) + float(value[1]) / 60.0 + float(value[2]) / 3600.0
    return d

# Function to extract EXIF data and show it in the Tkinter window
def extract_exif_data(image_path):
    exif_info = ""
    with Image.open(image_path) as img:
        exif_data = img._getexif()
        readable_exif = {}

        if exif_data:
            for tag_id, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                readable_exif[tag_name] = value
                exif_info += f"Tag: {tag_name}, Value: {value}\n"
            
            # Add GPS location info if available
            gps_info = extract_gps_info(readable_exif)
            exif_info += gps_info + "\n"
        else:
            exif_info = "No EXIF data found."

    return exif_info

# Function to generate a pixel-wise hash of the image
def generate_pixel_hash(image_path):
    with Image.open(image_path) as img:
        img_array = np.array(img)
        pixel_hash = hashlib.sha256(img_array).hexdigest()
        return f"Pixel-wise hash: {pixel_hash}"

# Function to add a red overlay to the image
def add_red_overlay(image_path, output_path):
    with Image.open(image_path) as img:
        overlay = Image.new('RGBA', img.size, (255, 0, 0, 100))  # Red overlay with transparency
        img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
        img_with_overlay.save(output_path)

# Function to browse and select image
def browse_image():
    global selected_image_path
    selected_image_path = filedialog.askopenfilename(filetypes=[('Images', '*.jpg *.jpeg *.png')])
    if selected_image_path:
        render_image(selected_image_path)

# Function to render image in the Tkinter window
def render_image(image_path):
    img = Image.open(image_path)
    img.thumbnail((500, 500))  # Resize for display
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk  # Keep a reference to prevent garbage collection

# Functions for each feature when buttons are clicked
def extract_exif_clicked():
    if selected_image_path:
        exif_data = extract_exif_data(selected_image_path)
        exif_display.delete(1.0, tk.END)
        exif_display.insert(tk.END, exif_data)
    else:
        show_popup("Please select an image first!")

def extract_gps_clicked():
    if selected_image_path:
        with Image.open(selected_image_path) as img:
            exif_data = img._getexif()
            readable_exif = {}
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                    readable_exif[tag_name] = value
                gps_info = extract_gps_info(readable_exif)
                show_popup(gps_info)
            else:
                show_popup("No EXIF data found.")
    else:
        show_popup("Please select an image first!")

def generate_hash_clicked():
    if selected_image_path:
        hash_value = generate_pixel_hash(selected_image_path)
        show_popup(hash_value)
    else:
        show_popup("Please select an image first!")

def add_overlay_clicked():
    if selected_image_path:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(current_dir, "overlayed_image.png")
        add_red_overlay(selected_image_path, output_path)
        render_image(output_path)
        show_popup("Red overlay added and image saved as 'overlayed_image.png'.")
    else:
        show_popup("Please select an image first!")

# New functions for added features
def noise_detection_clicked():
    if selected_image_path:
        noise_info = image_analysis.detect_noise(selected_image_path)
        show_popup(noise_info)
    else:
        show_popup("Please select an image first!")

def blurriness_detection_clicked():
    if selected_image_path:
        blur_info = image_analysis.detect_blurriness(selected_image_path)
        show_popup(blur_info)
    else:
        show_popup("Please select an image first!")

def histogram_analysis_clicked():
    if selected_image_path:
        histogram_info = image_analysis.analyze_histogram(selected_image_path)
        show_popup(histogram_info)
    else:
        show_popup("Please select an image first!")

# Function to show popup messages
def show_popup(message):
    messagebox.showinfo("Info", message)

# Main UI setup
root = tk.Tk()
root.title("Image Forensics Tool")
root.geometry("800x600")
root.configure(bg='#f0f0f0')

# Scrollable frame
scrollable_frame = tk.Frame(root)
scrollable_frame.pack(fill=tk.BOTH, expand=True)

# Canvas for scrollable area
canvas = tk.Canvas(scrollable_frame)
scrollable_canvas = tk.Frame(canvas)
scrollable_canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
scrollbar = tk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((0, 0), window=scrollable_canvas, anchor="nw")

# Browse button
browse_button = tk.Button(scrollable_canvas, text="Browse Image", command=browse_image, font=("Arial", 12), bg='#4CAF50', fg='white')
browse_button.pack(pady=10)

# Buttons for various features with different colors
buttons = [
    ("Extract EXIF", extract_exif_clicked, '#2196F3'),
    ("Extract GPS", extract_gps_clicked, '#FF9800'),
    ("Generate Pixel Hash", generate_hash_clicked, '#F44336'),
    ("Add Red Overlay", add_overlay_clicked, '#4CAF50'),
    ("Detect Noise", noise_detection_clicked, '#9C27B0'),
    ("Detect Blurriness", blurriness_detection_clicked, '#3F51B5'),
    ("Analyze Histogram", histogram_analysis_clicked, '#009688'),
]

for (label, command, color) in buttons:
    button = tk.Button(scrollable_canvas, text=label, command=command, font=("Arial", 12), bg=color, fg='white')
    button.pack(pady=10)

# EXIF extraction result display
exif_display = scrolledtext.ScrolledText(scrollable_canvas, width=100, height=20, font=("Arial", 10))
exif_display.pack(pady=20)

# Image display area
image_label = tk.Label(scrollable_canvas)
image_label.pack(pady=20)

# Global variable to hold the selected image path
selected_image_path = None

root.mainloop()
