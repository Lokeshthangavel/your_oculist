import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pickle
import os

class DataProcessor:
    def __init__(self, data_path):
        """Initialize the data processor with the path to the dataset."""
        self.data_path = data_path
        self.df = None
        self.vision_data = None
        self.model_RE = None
        self.model_LE = None
    
    def load_data(self):
        """Load and perform initial processing of the dataset."""
        self.df = pd.read_csv(self.data_path)
        
        # Extract relevant columns
        self.vision_data = self.df[[
            'Qn 1.3.1: Presenting distance vision at 6/12, RE', 
            'Qn 1.3.2:  Presenting distance vision at 6/12, LE',
            'Qn 1.4.1: Prescription distance, RE',
            'Qn 1.4.2: Prescription distance, LE',
            'Qn 1.5.1:  Corrected vision (Right eye)',
            'Qn 1.5.2: Corrected vision (Left eye)'
        ]].copy()
        
        # Rename columns for easier handling
        self.vision_data.columns = [
            'uncorrected_RE', 
            'uncorrected_LE',
            'prescription_RE',
            'prescription_LE',
            'corrected_RE',
            'corrected_LE'
        ]
        
        return self.vision_data
    
    def clean_data(self):
        """Clean the data and prepare it for modeling."""
        if self.vision_data is None:
            self.load_data()
        
        # Convert vision values to standard format
        self.vision_data['decimal_RE'] = self.vision_data['corrected_RE'].apply(self.snellen_to_decimal)
        self.vision_data['decimal_LE'] = self.vision_data['corrected_LE'].apply(self.snellen_to_decimal)
        
        # Clean prescription data
        self.vision_data['prescription_RE'] = pd.to_numeric(self.vision_data['prescription_RE'], errors='coerce')
        self.vision_data['prescription_LE'] = pd.to_numeric(self.vision_data['prescription_LE'], errors='coerce')
        
        # Drop rows with missing values in key columns
        self.vision_data = self.vision_data.dropna(subset=['prescription_RE', 'prescription_LE', 'decimal_RE', 'decimal_LE'])
        
        return self.vision_data
    
    @staticmethod
    def snellen_to_decimal(snellen_str):
        """Convert Snellen notation (e.g., '6/12') to decimal visual acuity."""
        if pd.isna(snellen_str) or snellen_str == '':
            return np.nan
        
        # Handle 'Pass'/'Fail' values
        if snellen_str == 'Pass':
            return 1.0  # Assuming 'Pass' means normal vision (6/6)
        if snellen_str == 'Fail':
            return 0.5  # Assuming 'Fail' means impaired vision (6/12)
        
        # Handle Snellen fractions
        if '/' in str(snellen_str):
            try:
                numerator, denominator = map(float, str(snellen_str).split('/'))
                return numerator / denominator
            except:
                return np.nan
        
        return np.nan
    
    @staticmethod
    def decimal_to_snellen(decimal):
        """Convert decimal visual acuity to Snellen notation."""
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
    
    def train_model(self):
        """Train regression models to predict prescription based on visual acuity."""
        if self.vision_data is None or 'decimal_RE' not in self.vision_data.columns:
            self.clean_data()
        
        # Prepare features and targets
        X_RE = self.vision_data[['decimal_RE']].values
        y_RE = self.vision_data['prescription_RE'].values
        
        X_LE = self.vision_data[['decimal_LE']].values
        y_LE = self.vision_data['prescription_LE'].values
        
        # Train models
        self.model_RE = LinearRegression()
        self.model_RE.fit(X_RE, y_RE)
        
        self.model_LE = LinearRegression()
        self.model_LE.fit(X_LE, y_LE)
        
        # Save models
        os.makedirs('model/saved_models', exist_ok=True)
        with open('model/saved_models/model_RE.pkl', 'wb') as f:
            pickle.dump(self.model_RE, f)
        
        with open('model/saved_models/model_LE.pkl', 'wb') as f:
            pickle.dump(self.model_LE, f)
        
        return self.model_RE, self.model_LE
    
    def visualize_data(self):
        """Create visualizations of the data and model predictions."""
        if self.vision_data is None or self.model_RE is None:
            self.train_model()
        
        # Create scatter plot of visual acuity vs prescription
        plt.figure(figsize=(12, 6))
        
        # Right eye
        plt.subplot(1, 2, 1)
        plt.scatter(self.vision_data['decimal_RE'], self.vision_data['prescription_RE'], alpha=0.6)
        
        # Plot regression line
        x_range = np.linspace(0, 1, 100).reshape(-1, 1)
        y_pred = self.model_RE.predict(x_range)
        plt.plot(x_range, y_pred, color='red', linewidth=2)
        
        plt.title('Right Eye: Visual Acuity vs Prescription')
        plt.xlabel('Visual Acuity (Decimal)')
        plt.ylabel('Prescription (Diopters)')
        plt.grid(True, alpha=0.3)
        
        # Left eye
        plt.subplot(1, 2, 2)
        plt.scatter(self.vision_data['decimal_LE'], self.vision_data['prescription_LE'], alpha=0.6)
        
        # Plot regression line
        x_range = np.linspace(0, 1, 100).reshape(-1, 1)
        y_pred = self.model_LE.predict(x_range)
        plt.plot(x_range, y_pred, color='red', linewidth=2)
        
        plt.title('Left Eye: Visual Acuity vs Prescription')
        plt.xlabel('Visual Acuity (Decimal)')
        plt.ylabel('Prescription (Diopters)')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save the plot
        os.makedirs('web/static/images', exist_ok=True)
        plt.savefig('web/static/images/vision_prescription_correlation.png')
        
        return plt