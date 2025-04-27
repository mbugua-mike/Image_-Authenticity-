import os
import numpy as np
import cv2
from PIL import Image, ImageDraw
import random
from datetime import datetime

def create_authentic_image(filename, with_exif=True):
    """Create an authentic-looking image with optional EXIF data"""
    # Create a simple image with a gradient
    img = np.zeros((400, 400, 3), dtype=np.uint8)
    
    # Add a gradient
    for i in range(400):
        for j in range(400):
            img[i, j] = [i % 256, j % 256, (i + j) % 256]
    
    # Add some random noise to make it look more natural
    noise = np.random.normal(0, 10, (400, 400, 3)).astype(np.uint8)
    img = cv2.add(img, noise)
    
    # Save the image
    cv2.imwrite(filename, img)
    
    if with_exif:
        # Add EXIF data using PIL
        img_pil = Image.open(filename)
        exif = img_pil.getexif()
        exif[0x010F] = "Sample Camera"  # Make
        exif[0x0110] = "Model X"        # Model
        exif[0x0132] = datetime.now().strftime("%Y:%m:%d %H:%M:%S")  # DateTime
        img_pil.save(filename, exif=exif)
    
    return filename

def create_compressed_image(original_filename, output_filename, quality=30):
    """Create a compressed version of an image"""
    img = cv2.imread(original_filename)
    cv2.imwrite(output_filename, img, [cv2.IMWRITE_JPEG_QUALITY, quality])
    return output_filename

def create_cloned_image(original_filename, output_filename):
    """Create an image with cloned regions"""
    img = cv2.imread(original_filename)
    height, width = img.shape[:2]
    
    # Clone a region
    clone_size = 100
    source_x = random.randint(0, width - clone_size)
    source_y = random.randint(0, height - clone_size)
    target_x = random.randint(0, width - clone_size)
    target_y = random.randint(0, height - clone_size)
    
    # Copy the region
    cloned_region = img[source_y:source_y+clone_size, source_x:source_x+clone_size].copy()
    img[target_y:target_y+clone_size, target_x:target_x+clone_size] = cloned_region
    
    cv2.imwrite(output_filename, img)
    return output_filename

def create_combined_manipulation(original_filename, output_filename):
    """Create an image with both compression and cloning"""
    # First create a cloned version
    temp_filename = "temp_cloned.jpg"
    create_cloned_image(original_filename, temp_filename)
    
    # Then compress it
    create_compressed_image(temp_filename, output_filename, quality=40)
    
    # Clean up temporary file
    os.remove(temp_filename)
    return output_filename

def main():
    # Create sample_images directory if it doesn't exist
    os.makedirs("sample_images", exist_ok=True)
    
    # Generate authentic images
    print("Generating authentic images...")
    authentic_1 = create_authentic_image("sample_images/authentic_1.jpg", with_exif=True)
    authentic_2 = create_authentic_image("sample_images/authentic_2.jpg", with_exif=True)
    authentic_3 = create_authentic_image("sample_images/authentic_3.jpg", with_exif=False)
    
    # Generate manipulated images
    print("Generating manipulated images...")
    manipulated_1 = create_compressed_image(authentic_1, "sample_images/manipulated_1.jpg", quality=30)
    manipulated_2 = create_cloned_image(authentic_2, "sample_images/manipulated_2.jpg")
    manipulated_3 = create_combined_manipulation(authentic_3, "sample_images/manipulated_3.jpg")
    
    print("Sample images generated successfully!")
    print("\nGenerated images:")
    print("1. Authentic images:")
    print(f"   - {authentic_1} (with complete EXIF data)")
    print(f"   - {authentic_2} (with minimal EXIF data)")
    print(f"   - {authentic_3} (with no EXIF data)")
    print("\n2. Manipulated images:")
    print(f"   - {manipulated_1} (compression artifacts)")
    print(f"   - {manipulated_2} (cloned regions)")
    print(f"   - {manipulated_3} (compression + cloning)")

if __name__ == "__main__":
    main() 