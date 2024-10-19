from PIL import Image
import numpy as np
import cv2

# Function to detect noise in an image
def detect_noise(image_path):
    img = Image.open(image_path).convert("L")
    img_array = np.array(img)

    # Calculate the variance of the Laplacian (noise measure)
    noise = cv2.Laplacian(img_array, cv2.CV_64F).var()

    if noise < 100:
        return f"Noise level is low. Variance: {noise:.2f}"
    else:
        return f"Noise level is high. Variance: {noise:.2f}"

# Function to detect blurriness in an image
def detect_blurriness(image_path):
    img = Image.open(image_path).convert("L")
    img_array = np.array(img)

    # Calculate the variance of the Laplacian (blurriness measure)
    blur = cv2.Laplacian(img_array, cv2.CV_64F).var()

    if blur < 100:
        return f"Image is blurry. Variance: {blur:.2f}"
    else:
        return f"Image is not blurry. Variance: {blur:.2f}"



# Function to check metadata integrity
def check_metadata_integrity(image_path):
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()  # Get EXIF data
            if not exif_data:
                return "No EXIF metadata found."

            # Convert the EXIF data to human-readable tags
            readable_exif = {}
            for tag_id, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                readable_exif[tag_name] = value

            if readable_exif:
                return "Metadata is present and intact.\n" + "\n".join(f"{tag}: {readable_exif[tag]}" for tag in readable_exif)
            else:
                return "No readable EXIF metadata found or metadata integrity compromised."
    
    except Exception as e:
        return f"Error checking metadata integrity: {str(e)}"


# Function to analyze the histogram of the image
def analyze_histogram(image_path):
    img = Image.open(image_path).convert("L")
    img_array = np.array(img)

    # Calculate histogram
    histogram, _ = np.histogram(img_array, bins=256, range=(0, 256))

    # Analyze the histogram and generate basic information
    max_value = np.max(histogram)
    min_value = np.min(histogram)
    mean_value = np.mean(histogram)

    return f"Histogram analysis:\nMax value: {max_value}\nMin value: {min_value}\nMean value: {mean_value:.2f}"

