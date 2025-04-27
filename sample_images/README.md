# Sample Images for Image Forgery Detection

This directory contains sample images for testing the image forgery detection system. The images are categorized as follows:

## Authentic Images
1. `authentic_1.jpg` - Original image with complete EXIF data
2. `authentic_2.jpg` - Original image with minimal EXIF data
3. `authentic_3.jpg` - Original image with no EXIF data

## Potentially Manipulated Images
1. `manipulated_1.jpg` - Image with compression artifacts
2. `manipulated_2.jpg` - Image with cloned regions
3. `manipulated_3.jpg` - Image with both compression artifacts and cloned regions

## Test Cases
- **Metadata Analysis**: Test EXIF data presence and integrity
- **Compression Analysis**: Test detection of compression artifacts
- **Region Analysis**: Test detection of cloned or duplicated regions
- **Combined Analysis**: Test detection of multiple manipulation types

## Usage
1. Upload these images to test different aspects of the forgery detection system
2. Compare results between authentic and manipulated images
3. Use for testing the system's accuracy and reliability

## Notes
- All images are provided for testing purposes only
- Images should be used in accordance with their respective licenses
- Some images may be marked as suspicious even if they are authentic, as this helps test the system's sensitivity 