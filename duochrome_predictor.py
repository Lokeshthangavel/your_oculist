import numpy as np
import math

class DuochromePredictor:
    def __init__(self):
        """Initialize the duochrome test predictor."""
        self.duochrome_interval_factor = 0.25  # Typical interval for duochrome tests
    
    def calculate_logmar(self, snellen_numerator, snellen_denominator, letters_correct=0):
        """Calculate LogMAR value from Snellen measurements and letter count."""
        logmar = math.log10(snellen_denominator / snellen_numerator) - (letters_correct * 0.02)
        return round(logmar, 2)
    
    def interpret_duochrome_result(self, red_clearer, green_clearer, equal_clarity):
        """
        Interpret duochrome test results to determine adjustment direction.
        
        Returns:
        - duochrome_adjustment: Factor to adjust sphere power (-1, 0, 1)
        """
        if equal_clarity:
            return 0  # No adjustment needed
        if red_clearer:
            return -1  # More minus needed (myopia)
        if green_clearer:
            return 1   # More plus needed (hyperopia)
        
        raise ValueError("❌ Invalid input: At least one of red_clearer, green_clearer, or equal_clarity must be True.")
    
    def get_duochrome_intensity(self, intensity_level):
        """
        Convert user-reported intensity level to adjustment magnitude.
        
        Returns:
        - intensity_factor: Scaling factor for the adjustment
        """
        intensity_map = {1: 0.25, 2: 0.5, 3: 0.75, 4: 1.0, 5: 1.25}
        return intensity_map.get(intensity_level, 0.5)  # Default to 0.5 if invalid
    
    def predict_adjustment(self, snellen_numerator, snellen_denominator, 
                           letters_correct, red_clearer, green_clearer, 
                           equal_clarity, intensity_level=3):
        """
        Predict adjustment based on duochrome test results.
        
        Returns:
        - adjustment: Suggested power adjustment in diopters (rounded to 0.25D)
        """
        try:
            duochrome_direction = self.interpret_duochrome_result(red_clearer, green_clearer, equal_clarity)
        except ValueError as e:
            return str(e)
        
        intensity_factor = self.get_duochrome_intensity(intensity_level)
        adjustment = duochrome_direction * intensity_factor * self.duochrome_interval_factor
        
        return round(adjustment * 4) / 4  # Round to nearest 0.25D

# Run a test case
if __name__ == "__main__":
    predictor = DuochromePredictor()
    
    # Test case: Red is clearer, Intensity 3 (Default)
    result = predictor.predict_adjustment(
        snellen_numerator=6, snellen_denominator=12, 
        letters_correct=0, 
        red_clearer=True, green_clearer=False, equal_clarity=False,
        intensity_level=3
    )
    print(f"Suggested Adjustment: {result} D")  # Example Output: -0.25D


    