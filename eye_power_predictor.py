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
        """Load the trained models from disk."""
        model_dir = 'model/saved_models'
        
        # Check if models exist
        if not os.path.exists(f'{model_dir}/model_RE.pkl'):
            raise FileNotFoundError("Models not found. Please train the models first.")
        
        # Load the models
        with open(f'{model_dir}/model_RE.pkl', 'rb') as f:
            self.model_RE = pickle.load(f)
        
        with open(f'{model_dir}/model_LE.pkl', 'rb') as f:
            self.model_LE = pickle.load(f)
    
    def predict(self, visual_acuity_re, visual_acuity_le):
        """
        Predict eye power based on visual acuity.
        
        Parameters:
        visual_acuity_re (float): Visual acuity of right eye in decimal format (0.0-1.0)
        visual_acuity_le (float): Visual acuity of left eye in decimal format (0.0-1.0)
        
        Returns:
        dict: Predicted eye power for both eyes
        """
        if self.model_RE is None or self.model_LE is None:
            self.load_models()
        
        # Make predictions
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
    def snellen_to_decimal(snellen):
        """
        Convert Snellen visual acuity to decimal format.
        
        Parameters:
        snellen (str): Visual acuity in Snellen format (e.g., '6/6', '6/12')
        
        Returns:
        float: Visual acuity in decimal format
        """
        if '/' not in snellen:
            return 0.5  # Default value if format is incorrect
        
        numerator, denominator = map(float, snellen.split('/'))
        return numerator / denominator
    
    @staticmethod
    def decimal_to_snellen(decimal):
        """
        Convert decimal visual acuity to Snellen format.
        
        Parameters:
        decimal (float): Visual acuity in decimal format (0.0-1.0)
        
        Returns:
        str: Visual acuity in Snellen format
        """
        if decimal >= 1.0:
            return "6/6"
        elif decimal >= 0.8:
            return "6/7.5"
        elif decimal >= 0.67:
            return "6/9"
        elif decimal >= 0.5:
            return "6/12"
        elif decimal >= 0.33:
            return "6/18"
        elif decimal >= 0.25:
            return "6/24"
        elif decimal >= 0.1:
            return "6/60"
        else:
            return "< 6/60"