import joblib
from model.eye_power_predictor import EyePowerPredictor  # Ensure correct import

# Initialize the model
model = EyePowerPredictor()  

# Save the trained model
joblib.dump(model, "eye_power_model.pkl")  

print("Model saved successfully as eye_power_model.pkl")