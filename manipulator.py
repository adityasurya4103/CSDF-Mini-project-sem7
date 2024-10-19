from PIL import Image, ImageDraw

def manipulate_image(image_path, output_path):
    with Image.open(image_path) as img:
        # Create a new image with the same mode and size
        manipulated_img = Image.new(img.mode, img.size)
        # Paste the original image into the new one
        manipulated_img.paste(img)
        
        # Create a red overlay (RGBA mode for transparency)
        red_overlay = Image.new("RGBA", img.size, (255, 0, 0, 100))
        
        # Combine the original image with the red overlay
        manipulated_img = Image.alpha_composite(manipulated_img.convert("RGBA"), red_overlay)
        
        # Save the manipulated image to the specified output path
        manipulated_img.save(output_path)


def manipulate(image_path, save_path):
    with Image.open(image_path) as img:
        # Add a red overlay
        overlay = Image.new('RGBA', img.size, (255, 0, 0, 100))  # Red overlay with transparency
        img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
        img_with_overlay.save(save_path)  # Save to the specified path
