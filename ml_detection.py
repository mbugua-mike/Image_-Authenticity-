import cv2
import numpy as np
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image

class ForgeryDetector(nn.Module):
    def __init__(self):
        super(ForgeryDetector, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(128 * 28 * 28, 512)
        self.fc2 = nn.Linear(512, 2)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)
        
    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        x = x.view(-1, 128 * 28 * 28)
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

def load_model():
    """Load the pre-trained forgery detection model"""
    try:
        model = ForgeryDetector()
        # In a real application, you would load pre-trained weights here
        # model.load_state_dict(torch.load('model_weights.pth'))
        model.eval()
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None

def preprocess_image(image_path):
    """Preprocess the image for the model"""
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)
    return image

def detect_forgery_ml(image_path, model):
    """Detect image forgery using machine learning and traditional methods"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return {'error': 'Could not read image'}
        
        # Initialize results dictionary
        results = {
            'ml_confidence': None,
            'compression_artifacts': False,
            'suspicious_regions': False,
            'analysis_details': {
                'compression_score': 0.0,
                'cloning_score': 0,
                'ml_probability': None
            }
        }
        
        # Check for compression artifacts
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dct = cv2.dct(np.float32(gray))
        compression_score = np.mean(np.abs(dct))
        results['analysis_details']['compression_score'] = float(compression_score)
        results['compression_artifacts'] = compression_score > 0.1
        
        # Check for cloning/duplication
        sift = cv2.SIFT_create()
        keypoints, descriptors = sift.detectAndCompute(gray, None)
        cloning_score = len(keypoints)
        results['analysis_details']['cloning_score'] = int(cloning_score)
        results['suspicious_regions'] = cloning_score > 1000
        
        # If ML model is available, get its prediction
        if model is not None:
            try:
                # Preprocess image for ML model
                image = preprocess_image(image_path)
                with torch.no_grad():
                    output = model(image)
                    probabilities = torch.softmax(output, dim=1)
                    forgery_prob = probabilities[0][1].item()
                results['ml_confidence'] = float(forgery_prob)
                results['analysis_details']['ml_probability'] = float(forgery_prob)
            except Exception as e:
                print(f"ML model prediction failed: {str(e)}")
                # Continue with traditional analysis results
        
        return results
        
    except Exception as e:
        return {'error': str(e)}

def analyze_image_regions(image_path):
    """Analyze different regions of the image for inconsistencies"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return {'error': 'Could not read image'}
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply edge detection
        edges = cv2.Canny(gray, 100, 200)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Analyze regions
        regions = []
        for i, contour in enumerate(contours[:5]):  # Analyze top 5 regions
            x, y, w, h = cv2.boundingRect(contour)
            region = gray[y:y+h, x:x+w]
            
            # Calculate region statistics
            mean = np.mean(region)
            std = np.std(region)
            entropy = -np.sum(region * np.log2(region + 1e-10))
            
            regions.append({
                'region_id': i,
                'position': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)},
                'statistics': {
                    'mean': float(mean),
                    'std': float(std),
                    'entropy': float(entropy)
                }
            })
        
        return {'regions': regions}
        
    except Exception as e:
        return {'error': str(e)} 