from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from PIL import Image
from exif import Image as ExifImage
import magic
import json
from datetime import datetime
import traceback
from ml_detection import load_model, detect_forgery_ml, analyze_image_regions
from report_generator import generate_report

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['REPORTS_FOLDER'] = 'reports'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload and reports directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)

# Store analysis results
analysis_results = {}

# Load ML model
try:
    model = load_model()
except Exception as e:
    print(f"Error loading ML model: {str(e)}")
    model = None

def analyze_metadata(image_path):
    """Analyze image metadata"""
    try:
        with open(image_path, 'rb') as image_file:
            img = ExifImage(image_file)
        
        metadata = {
            'has_exif': img.has_exif,
            'make': img.get('make', ''),
            'model': img.get('model', ''),
            'datetime': img.get('datetime', ''),
            'software': img.get('software', '')
        }
        return metadata
    except Exception as e:
        return {'error': str(e)}

def convert_numpy_types(obj):
    """Convert NumPy types to Python native types for JSON serialization"""
    if isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    return obj

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Check file type
        mime = magic.Magic(mime=True)
        file_mime = mime.from_buffer(file.read(1024))
        file.seek(0)  # Reset file pointer
        
        if not file_mime.startswith('image/'):
            return jsonify({'error': 'File must be an image'}), 400
        
        # Ensure upload directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analyze metadata
        metadata = analyze_metadata(filepath)
        if isinstance(metadata, dict) and 'error' in metadata:
            return jsonify({'error': f'Metadata analysis failed: {metadata["error"]}'}), 500
        
        # Detect forgery using ML
        forgery_detection = {'error': 'ML model not loaded'} if model is None else detect_forgery_ml(filepath, model)
        if isinstance(forgery_detection, dict) and 'error' in forgery_detection:
            return jsonify({'error': f'Forgery detection failed: {forgery_detection["error"]}'}), 500
        
        # Analyze image regions
        region_analysis = analyze_image_regions(filepath)
        if isinstance(region_analysis, dict) and 'error' in region_analysis:
            return jsonify({'error': f'Region analysis failed: {region_analysis["error"]}'}), 500
        
        # Store results
        results = {
            'filename': filename,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'metadata': metadata,
            'forgery_detection': forgery_detection,
            'region_analysis': region_analysis
        }
        
        # Convert NumPy types to Python native types
        results = convert_numpy_types(results)
        analysis_results[filename] = results
        
        # Return results
        return jsonify(results)
        
    except Exception as e:
        app.logger.error(f"Error processing file: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/generate_report/<filename>')
def generate_pdf_report(filename):
    try:
        if filename not in analysis_results:
            return jsonify({'error': 'Analysis results not found for this image'}), 404
        
        # Generate report filename
        report_filename = f"report_{filename.rsplit('.', 1)[0]}.pdf"
        report_path = os.path.join(app.config['REPORTS_FOLDER'], report_filename)
        
        # Get image path
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Generate PDF report
        generate_report(image_path, analysis_results[filename], report_path)
        
        # Return the PDF file
        return send_from_directory(
            app.config['REPORTS_FOLDER'],
            report_filename,
            as_attachment=True,
            download_name=report_filename
        )
        
    except Exception as e:
        app.logger.error(f"Error generating report: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': f'Error generating report: {str(e)}'}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=False) 