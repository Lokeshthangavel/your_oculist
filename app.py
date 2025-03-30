from flask import Flask, render_template, request, redirect, url_for
import os
import numpy as np
from model.data_processor import DataProcessor
from model.eye_power_predictor import EyePowerPredictor

app = Flask(__name__, static_folder='web/static', template_folder='web/templates')

# Initialize the models
@app.before_first_request
def initialize():
    # Check if models exist, if not, train them
    if not os.path.exists('model/saved_models/model_RE.pkl'):
        print("Training models...")
        data_path = 'data/Phase_1_WE_ZACE_prevalence_and_attiitudes.csv'
        processor = DataProcessor(data_path)
        processor.load_data()
        processor.clean_data()
        processor.train_model()
        processor.visualize_data()
        print("Models trained successfully!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/estimate', methods=['POST'])
def estimate():
    # Get form data
    right_eye = request.form.get('right_eye')
    left_eye = request.form.get('left_eye')
    
    # Convert Snellen values to decimal
    right_eye_decimal = EyePowerPredictor.snellen_to_decimal(right_eye)
    left_eye_decimal = EyePowerPredictor.snellen_to_decimal(left_eye)
    
    # Make prediction
    predictor = EyePowerPredictor()
    results = predictor.predict(right_eye_decimal, left_eye_decimal)
    
    # Render results template
    return render_template('result.html', 
                          results=results,
                          snellen_values={'right_eye': right_eye, 'left_eye': left_eye})

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('model/saved_models', exist_ok=True)
    os.makedirs('web/static/images', exist_ok=True)
    
    # Start the Flask app
    app.run(debug=True)