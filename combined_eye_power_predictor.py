import numpy as np
import os
from model.eye_power_predictor import EyePowerPredictor
from model.duochrome_predictor import DuochromePredictor

class CombinedEyePowerPredictor:
    def __init__(self, snellen_weight=0.7, duochrome_weight=0.3):
        """Initialize the combined eye power predictor with adjustable weights."""
        self.snellen_predictor = EyePowerPredictor()
        self.duochrome_predictor = DuochromePredictor()
        
        # Ensure weights sum to 1
        total_weight = snellen_weight + duochrome_weight
        self.snellen_weight = snellen_weight / total_weight
        self.duochrome_weight = duochrome_weight / total_weight
    
    def predict(self, eye_data):
        """
        Predict eye power using combined model of Snellen VA and duochrome test.
        
        Parameters:
        - eye_data: Dictionary with:
            - 'visual_acuity_re': Decimal VA for right eye (e.g., 0.5)
            - 'visual_acuity_le': Decimal VA for left eye (e.g., 0.67)
            - 'snellen_re': Dict with numerator/denominator for right eye
            - 'snellen_le': Dict with numerator/denominator for left eye
            - 'duochrome_re': Dict with duochrome test results for right eye
            - 'duochrome_le': Dict with duochrome test results for left eye
        
        Returns:
        - Dictionary with predicted prescription and confidence levels
        """
        # Get base predictions from Snellen model
        snellen_predictions = self.snellen_predictor.predict(
            eye_data['visual_acuity_re'], 
            eye_data['visual_acuity_le']
        )
        
        # Calculate duochrome adjustments
        re_adjustment = self._get_duochrome_adjustment(
            eye_data['snellen_re'], 
            eye_data['duochrome_re']
        )
        
        le_adjustment = self._get_duochrome_adjustment(
            eye_data['snellen_le'], 
            eye_data['duochrome_le']
        )
        
        # Combine predictions
        re_combined = (self.snellen_weight * snellen_predictions['right_eye'] + 
                      self.duochrome_weight * (snellen_predictions['right_eye'] + re_adjustment))
        
        le_combined = (self.snellen_weight * snellen_predictions['left_eye'] + 
                      self.duochrome_weight * (snellen_predictions['left_eye'] + le_adjustment))
        
        # Round to nearest 0.25 diopter
        re_combined = round(re_combined * 4) / 4
        le_combined = round(le_combined * 4) / 4
        
        # Calculate confidence levels based on agreement between models
        re_confidence = self._calculate_confidence(snellen_predictions['right_eye'], 
                                                  snellen_predictions['right_eye'] + re_adjustment)
        
        le_confidence = self._calculate_confidence(snellen_predictions['left_eye'], 
                                                  snellen_predictions['left_eye'] + le_adjustment)
        
        return {
            'right_eye': {
                'prescription': re_combined,
                'snellen_prediction': snellen_predictions['right_eye'],
                'duochrome_adjustment': re_adjustment,
                'confidence': re_confidence
            },
            'left_eye': {
                'prescription': le_combined,
                'snellen_prediction': snellen_predictions['left_eye'],
                'duochrome_adjustment': le_adjustment,
                'confidence': le_confidence
            }
        }
    
    def _get_duochrome_adjustment(self, snellen_data, duochrome_data):
        """Calculate adjustment based on duochrome test for a single eye."""
        return self.duochrome_predictor.predict_adjustment(
            snellen_data['numerator'],
            snellen_data['denominator'],
            duochrome_data.get('letters_correct', 0),
            duochrome_data['red_clearer'],
            duochrome_data['green_clearer'],
            duochrome_data['equal_clarity'],
            duochrome_data['intensity_level']
        )
    
    def _calculate_confidence(self, snellen_prediction, duochrome_prediction):
        """Calculate confidence level based on agreement between models."""
        difference = abs(snellen_prediction - duochrome_prediction)
        
        if difference < 0.5:  # Adjusted threshold for clinical settings
            return "High"
        elif difference < 1.0:
            return "Medium"
        else:
            return "Low"
    
    @staticmethod
    def prepare_input_data(snellen_re, snellen_le, duochrome_re, duochrome_le):
        """
        Prepare and validate input data for prediction.
        
        Parameters:
        - snellen_re: String Snellen fraction for right eye (e.g., "6/12")
        - snellen_le: String Snellen fraction for left eye (e.g., "6/9")
        - duochrome_re: Dict with duochrome test results for right eye
        - duochrome_le: Dict with duochrome test results for left eye
        
        Returns:
        - Dictionary with processed input data
        """
        try:
            re_num, re_denom = map(int, snellen_re.split('/'))
            le_num, le_denom = map(int, snellen_le.split('/'))
        except ValueError:
            raise ValueError("Invalid Snellen format! Use format like '6/12'.")
        
        # Ensure at least one duochrome test result is selected
        for eye_data in [duochrome_re, duochrome_le]:
            if not (eye_data['red_clearer'] or eye_data['green_clearer'] or eye_data['equal_clarity']):
                raise ValueError("Duochrome test results missing! Please select an option.")

        visual_acuity_re = re_num / re_denom
        visual_acuity_le = le_num / le_denom
        
        return {
            'visual_acuity_re': visual_acuity_re,
            'visual_acuity_le': visual_acuity_le,
            'snellen_re': {'numerator': re_num, 'denominator': re_denom},
            'snellen_le': {'numerator': le_num, 'denominator': le_denom},
            'duochrome_re': duochrome_re,
            'duochrome_le': duochrome_le
        }


# Example usage
if __name__ == "__main__":
    predictor = CombinedEyePowerPredictor()
    
    # Example data
    eye_data = {
        'visual_acuity_re': 0.5,  # 6/12
        'visual_acuity_le': 0.67,  # 6/9
        'snellen_re': {'numerator': 6, 'denominator': 12},
        'snellen_le': {'numerator': 6, 'denominator': 9},
        'duochrome_re': {
            'red_clearer': True,
            'green_clearer': False,
            'equal_clarity': False,
            'intensity_level': 3,
            'letters_correct': 0
        },
        'duochrome_le': {
            'red_clearer': False,
            'green_clearer': True,
            'equal_clarity': False,
            'intensity_level': 2,
            'letters_correct': 1
        }
    }
    
    result = predictor.predict(eye_data)
    print(result)

predictor = CombinedEyePowerPredictor()

eye_data = {
    'visual_acuity_re': 0.5,  # 6/12
    'visual_acuity_le': 0.67,  # 6/9
    'snellen_re': {'numerator': 6, 'denominator': 12},
    'snellen_le': {'numerator': 6, 'denominator': 9},
    'duochrome_re': {
        'red_clearer': True,
        'green_clearer': False,
        'equal_clarity': False,
        'intensity_level': 3,
        'letters_correct': 0
    },
    'duochrome_le': {
        'red_clearer': False,
        'green_clearer': True,
        'equal_clarity': False,
        'intensity_level': 2,
        'letters_correct': 1
    }
}

result = predictor.predict(eye_data)
print(result)