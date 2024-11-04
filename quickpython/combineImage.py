"""
Usage:
    python combineImage.py <image1_path> <image2_path> <output_path>

Arguments:
    image1_path : str : Path to the first image file.
    image2_path : str : Path to the second image file.
    output_path : str : Path where the combined image will be saved.

Example:
    python combineImage.py image1.jpg image2.jpg combined_image.jpg

Description:
    This script combines two images side by side with a 5-pixel divider between them.
    The images are resized to have the same height if they are different.
    The combined image is saved to the specified output path.
"""

import argparse
from PIL import Image

def combine_images(image1_path, image2_path, output_path):
    try:
        # Load images
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)
    except IOError as e:
        print(f"Error opening image files: {e}")
        return
    
    # Resize images to the same height
    new_height = min(image1.height, image2.height)
    if image1.height != new_height:
        image1 = image1.resize((int(image1.width * new_height / image1.height), new_height))
    if image2.height != new_height:
        image2 = image2.resize((int(image2.width * new_height / image2.height), new_height))
    
    # Create a new image with combined width, same height, and a 5-pixel divider
    divider_width = 5
    combined_width = image1.width + image2.width + divider_width
    combined_image = Image.new('RGB', (combined_width, new_height))
    
    # Paste images side by side with a 5-pixel divider
    combined_image.paste(image1, (0, 0))
    combined_image.paste(image2, (image1.width + divider_width, 0))
    
    try:
        # Save the combined image
        combined_image.save(output_path)
        print(f"Combined image saved to {output_path}")
    except IOError as e:
        print(f"Error saving combined image: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine two images side by side with a 5-pixel divider.")
    parser.add_argument("image1", help="Path to the first image")
    parser.add_argument("image2", help="Path to the second image")
    parser.add_argument("output", help="Path to save the combined image")
    
    args = parser.parse_args()
    
    combine_images(args.image1, args.image2, args.output)