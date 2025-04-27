# Image Forgery Detection System

A comprehensive system for detecting various forms of image forgery through metadata analysis and image processing techniques.

## Features

- User-friendly web interface for image upload and analysis
- Metadata analysis to detect inconsistencies in image information
- Detection of compression artifacts and suspicious regions
- Detailed analysis reports
- Support for drag-and-drop image uploads

## Requirements

- Python 3.8 or higher
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd image-forgery-detection
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Upload an image by either:
   - Dragging and dropping an image file onto the drop zone
   - Clicking the drop zone to select an image file

4. View the analysis results, which include:
   - File information
   - Metadata analysis
   - Forgery detection results

## Detection Methods

The system uses multiple techniques to detect potential image forgeries:

1. **Metadata Analysis**
   - EXIF data verification
   - Camera information validation
   - Timestamp analysis

2. **Image Processing**
   - Compression artifact detection
   - Suspicious region identification
   - Pattern analysis

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 