from PIL import Image
from PIL.ExifTags import TAGS

def extract_exif_data(image_path):
    """Extract EXIF data from an image."""
    with Image.open(image_path) as img:
        exif_data = img._getexif()
        if exif_data is not None:
            readable_exif = {TAGS.get(tag_id, tag_id): value for tag_id, value in exif_data.items()}
            return readable_exif
        return None
