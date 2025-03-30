# AI-Based Non-Invasive Eye Power Estimation  

##  Project Overview  
AI-Based Non-Invasive Eye Power Estimation is a machine learning-based system that estimates eye power using a smartphone camera. This solution aims to provide a quick, accessible, and non-invasive method for eye power detection without the need for conventional eye tests.  

## Features  
- **Real-time Eye Power Estimation** using image processing and AI.  
- **Non-invasive Approach** for easy and safe detection.  
- **Smartphone Camera Integration** to capture eye images.  
- **Machine Learning Model** for accurate power prediction.  
- **User-Friendly Interface** with quick results.  

##  Technologies Used  
- **Programming Languages:** Python, JavaScript (for web integration)  
- **Frameworks & Libraries:** OpenCV, TensorFlow, MediaPipe  
- **APIs Used:**  
  - Google Cloud Vision API (for image analysis)  
  - MediaPipe Face Mesh API (for eye landmark detection)  
  - Tesseract OCR (for extracting prescription details)  
  - Android CameraX / iOS Vision Framework (for capturing images)  
- **Cloud & Deployment:** Google AI Platform, Flask (API for model inference)  

##  How It Works  
1. **Capture Eye Image** using a smartphone camera.  
2. **Preprocess Image** (detect eyes, adjust lighting, and remove noise).  
3. **Apply AI Model** to estimate refractive error and suggest power.  
4. **Display Results** with recommended corrective lenses.  

##  Setup & Installation  
### **Prerequisites**  
- Python 3.8+  
- TensorFlow & OpenCV  
- Flask (for backend API)  
- Google Cloud Vision API Key  

### **Installation Steps**  
```bash
# Clone the repository
git clone https://github.com/your-username/eye-power-estimation.git
cd eye-power-estimation  

# Install dependencies
pip install -r requirements.txt  

# Run the application
python app.py

