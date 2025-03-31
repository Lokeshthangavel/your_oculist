import pandas as pd
import numpy as np
import os
import pickle
import logging
from sklearn.linear_model import LinearRegression

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DataProcessor:
    def __init__(self, data_path=None):
        """Initialize the DataProcessor with dataset path."""
        base_dir = os.path.dirname(__file__)  # Get script directory
        self.data_path = "/Users/lokeshthangavel/Documents/loki_coding/Your Oculist/data/dataset1.csv"
        self.df = None
        self.vision_data = None
        self.model_RE = None
        self.model_LE = None
    
    def load_data(self):
        """Load dataset with appropriate encoding."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"🚨 Dataset not found at {self.data_path}")

        try:
            self.df = pd.read_csv(self.data_path, encoding='ISO-8859-1', encoding_errors='replace')
        except UnicodeDecodeError:
            self.df = pd.read_csv(self.data_path, encoding='latin1', errors='replace')

        # Extract relevant columns safely
        required_columns = [
            'Qn 1.3.1: Presenting distance vision at 6/12, RE', 
            'Qn 1.3.2:  Presenting distance vision at 6/12, LE',
            'Qn 1.4.1: Prescription distance, RE',
            'Qn 1.4.2: Prescription distance, LE',
            'Qn 1.5.1:  Corrected vision (Right eye)',
            'Qn 1.5.2: Corrected vision (Left eye)'
        ]

        missing_cols = [col for col in required_columns if col not in self.df.columns]
        if missing_cols:
            logging.error(f"🚨 Missing columns in dataset: {missing_cols}")
            raise KeyError(f"Dataset is missing required columns: {missing_cols}")

        # Rename for easier access
        self.vision_data = self.df[required_columns].copy()
        self.vision_data.columns = [
            'uncorrected_RE', 'uncorrected_LE',
            'prescription_RE', 'prescription_LE',
            'corrected_RE', 'corrected_LE'
        ]
        
        return self.vision_data
    
    def clean_data(self):
        """Clean data and handle missing values."""
        if self.vision_data is None:
            self.load_data()
        
        # Convert vision values to decimal
        self.vision_data['decimal_RE'] = self.vision_data['corrected_RE'].apply(self.snellen_to_decimal)
        self.vision_data['decimal_LE'] = self.vision_data['corrected_LE'].apply(self.snellen_to_decimal)
        
        # Convert prescription values to numeric
        self.vision_data['prescription_RE'] = pd.to_numeric(self.vision_data['prescription_RE'], errors='coerce')
        self.vision_data['prescription_LE'] = pd.to_numeric(self.vision_data['prescription_LE'], errors='coerce')
        
        # Drop rows with missing values
        self.vision_data.dropna(subset=['prescription_RE', 'prescription_LE', 'decimal_RE', 'decimal_LE'], inplace=True)
        
        return self.vision_data
    
    @staticmethod
    def snellen_to_decimal(snellen_str):
        """Convert Snellen fraction to decimal visual acuity."""
        conversion_map = {
            'NPL': 0.0,  # No Perception of Light
            'PL': 0.05,  # Perception of Light
            'CF': 0.1,   # Counting Fingers
            'HM': 0.2,   # Hand Movement
            'Pass': 1.0,
            'Fail': 0.5
        }

        if pd.isna(snellen_str) or snellen_str == '':
            return np.nan
        
        if snellen_str in conversion_map:
            return conversion_map[snellen_str]

        if '/' in str(snellen_str):
            try:
                numerator, denominator = map(float, str(snellen_str).split('/'))
                return numerator / denominator
            except:
                return np.nan
        
        return np.nan
    
    def train_model(self):
        """Train regression models to predict prescription power."""
        if self.vision_data is None or 'decimal_RE' not in self.vision_data.columns:
            self.clean_data()
        
        X_RE = self.vision_data[['decimal_RE']].values
        y_RE = self.vision_data['prescription_RE'].values
        X_LE = self.vision_data[['decimal_LE']].values
        y_LE = self.vision_data['prescription_LE'].values
        
        # Train models
        self.model_RE = LinearRegression().fit(X_RE, y_RE)
        self.model_LE = LinearRegression().fit(X_LE, y_LE)
        
        # Save models
        model_dir = os.path.join(os.path.dirname(__file__), "model", "saved_models")
        os.makedirs(model_dir, exist_ok=True)
        
        try:
            with open(os.path.join(model_dir, 'model_RE.pkl'), 'wb') as f:
                pickle.dump(self.model_RE, f)
            with open(os.path.join(model_dir, 'model_LE.pkl'), 'wb') as f:
                pickle.dump(self.model_LE, f)
            logging.info("✅ Models trained and saved successfully!")
        except Exception as e:
            logging.error(f"🚨 Error saving models: {e}")

        return self.model_RE, self.model_LE


# Run training if executed directly
if __name__ == "__main__":
    processor = DataProcessor()
    processor.train_model()
