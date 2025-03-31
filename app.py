from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib  # Load your trained model

app = Flask(__name__)

# Load the pre-trained model
model = joblib.load("eye_power_model.pkl")  # Ensure your model is in the correct path

def calculate_eye_power(snellen_score, duochrome_result):
    """
    Function to predict eye power based on Snellen score and duochrome results.
    """
    input_data = np.array([[snellen_score, duochrome_result]])
    prediction = model.predict(input_data)
    return prediction[0]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract form data
        right_eye = int(request.form.get('right_eye'))
        left_eye = int(request.form.get('left_eye'))
        duochrome = int(request.form.get('duochrome'))
        
        # Compute eye power for both eyes
        right_eye_power = calculate_eye_power(right_eye, duochrome)
        left_eye_power = calculate_eye_power(left_eye, duochrome)
        
        result = {
            "right_eye_power": round(right_eye_power, 2),
            "left_eye_power": round(left_eye_power, 2)
        }
        
        return render_template('results.html', result=result)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
