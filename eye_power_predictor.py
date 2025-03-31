import pickle
import numpy as np
import os

class EyePowerPredictor:
    def __init__(self):
        """Initialize the eye power predictor model."""
        self.model_RE = None
        self.model_LE = None
        self.load_models()
    
    def load_models(self):
        """Load trained models from disk."""
        model_dir = 'model/saved_models'
        
        if not os.path.exists(f'{model_dir}/model_RE.pkl') or not os.path.exists(f'{model_dir}/model_LE.pkl'):
            raise FileNotFoundError("❌ Models not found! Train the models first.")
        
        try:
            with open(f'{model_dir}/model_RE.pkl', 'rb') as f:
                self.model_RE = pickle.load(f)
            with open(f'{model_dir}/model_LE.pkl', 'rb') as f:
                self.model_LE = pickle.load(f)
        except (pickle.UnpicklingError, EOFError) as e:
            raise RuntimeError("❌ Error loading models! They might be corrupted.") from e
    
    def predict(self, visual_acuity_re, visual_acuity_le):
        """Predict eye power based on visual acuity."""
        if self.model_RE is None or self.model_LE is None:
            self.load_models()
        
        prescription_re = float(self.model_RE.predict([[visual_acuity_re]])[0])
        prescription_le = float(self.model_LE.predict([[visual_acuity_le]])[0])
        
        # Round to nearest 0.25 diopter
        prescription_re = round(prescription_re * 4) / 4
        prescription_le = round(prescription_le * 4) / 4
        
        return {
            'right_eye': prescription_re,
            'left_eye': prescription_le
        }
    
    @staticmethod
    def snellen_to_decimal(snellen_value):
        """Converts Snellen fraction (e.g., 6/6) to a decimal value (e.g., 1.0)."""
        try:
            num, denom = map(int, snellen_value.split('/'))
            return num / denom  # Example: 6/12 -> 0.5
        except (ValueError, AttributeError):
            return None  # Return None if invalid input
    
# Run a test prediction
if __name__ == "__main__":
    predictor = EyePowerPredictor()
    print(predictor.predict(0.5, 0.67))  # Example
