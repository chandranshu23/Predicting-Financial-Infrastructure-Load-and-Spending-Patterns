"""
Model Service for Loading and Running Forecasts
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import pandas as pd
import joblib
import os
from datetime import datetime, timedelta

class AttentionLSTM(nn.Module):
    """Attention-based LSTM model architecture"""
    def __init__(self, input_size, hidden_size, num_layers, dropout=0.2):
        super(AttentionLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        # Bi-LSTM
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, 
                            batch_first=True, dropout=dropout, bidirectional=True)
        
        # Attention Layer
        self.attention_fc = nn.Linear(hidden_size * 2, 1)
        
        # Final Prediction
        self.fc = nn.Linear(hidden_size * 2, 1)

    def forward(self, x):
        # LSTM Output: (Batch, Seq_Len, Hidden*2)
        lstm_out, _ = self.lstm(x)
        
        # Attention Mechanism
        energy = torch.tanh(self.attention_fc(lstm_out))
        weights = F.softmax(energy, dim=1)
        context_vector = torch.sum(weights * lstm_out, dim=1)
        
        # Final Prediction
        out = self.fc(context_vector)
        return out


class ModelService:
    """Service for loading model and making predictions"""
    
    def __init__(self, model_dir='models'):
        self.model_dir = model_dir
        self.model = None
        self.target_scaler = None
        self.time_scaler = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.seq_length = 48
        self.historical_data = None
        self.is_model_loaded = False
        
        # Try to load model
        self._load_model()
    
    def _load_model(self):
        """Load the trained model and scalers"""
        try:
            model_path = os.path.join(self.model_dir, 'attention_lstm.pth')
            target_scaler_path = os.path.join(self.model_dir, 'target_scaler.pkl')
            time_scaler_path = os.path.join(self.model_dir, 'time_scaler.pkl')
            
            if not all(os.path.exists(p) for p in [model_path, target_scaler_path, time_scaler_path]):
                print(f"⚠️  Model files not found in {self.model_dir}")
                print("   Please ensure attention_lstm.pth, target_scaler.pkl, and time_scaler.pkl exist")
                return
            
            # Load scalers
            self.target_scaler = joblib.load(target_scaler_path)
            self.time_scaler = joblib.load(time_scaler_path)
            
            # Initialize and load model
            self.model = AttentionLSTM(input_size=5, hidden_size=128, num_layers=2)
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.to(self.device)
            self.model.eval()
            
            self.is_model_loaded = True
            print(f"✅ Model loaded successfully on {self.device}")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.is_model_loaded = False
    
    def is_loaded(self):
        """Check if model is loaded"""
        return self.is_model_loaded
    
    def _prepare_features(self, timestamp, historical_counts):
        """
        Prepare features for prediction
        Features: [transaction_count, lag_24, lag_168, hour, dayofweek]
        """
        hour = timestamp.hour
        dayofweek = timestamp.dayofweek
        
        # Get lag values from historical data
        lag_24 = historical_counts[-24] if len(historical_counts) >= 24 else historical_counts[-1]
        lag_168 = historical_counts[-168] if len(historical_counts) >= 168 else historical_counts[-1]
        current_count = historical_counts[-1]
        
        # Create feature array
        features = np.array([[current_count, lag_24, lag_168, hour, dayofweek]])
        
        # Scale features
        scaled_counts = self.target_scaler.transform(features[:, 0:3])
        scaled_time = self.time_scaler.transform(features[:, 3:])
        scaled_features = np.hstack((scaled_counts, scaled_time))
        
        return scaled_features
    
    def _generate_historical_data(self, start_timestamp, current_load=None):
        """
        Generate synthetic historical data if not available
        In production, this would come from a database
        """
        # Generate 200 hours of historical data (enough for lag_168)
        hours_back = 200
        timestamps = pd.date_range(
            start=start_timestamp - timedelta(hours=hours_back),
            end=start_timestamp - timedelta(hours=1),
            freq='h'
        )
        
        if current_load is not None:
            # Use current_load as baseline and add some variation
            base_load = current_load
        else:
            # Default baseline
            base_load = 1000
        
        # Generate synthetic data with daily and weekly patterns
        historical = []
        for ts in timestamps:
            hour_factor = 1.0 + 0.3 * np.sin(2 * np.pi * ts.hour / 24)
            day_factor = 1.0 + 0.2 * np.sin(2 * np.pi * ts.dayofweek / 7)
            noise = np.random.normal(0, 0.1)
            load = max(100, base_load * hour_factor * day_factor * (1 + noise))
            historical.append(load)
        
        return historical
    
    def forecast(self, hours_ahead=24, current_load=None, start_timestamp=None):
        """
        Generate forecast for the next N hours
        
        Args:
            hours_ahead: Number of hours to forecast
            current_load: Current transaction count (optional)
            start_timestamp: Start timestamp for forecast (defaults to now)
        
        Returns:
            Dictionary with forecast data
        """
        if not self.is_model_loaded:
            raise ValueError("Model not loaded. Please ensure model files exist.")
        
        if start_timestamp is None:
            start_timestamp = pd.Timestamp.now()
        else:
            start_timestamp = pd.Timestamp(start_timestamp)
        
        # Generate or use historical data
        historical_counts = self._generate_historical_data(start_timestamp, current_load)
        
        # Generate forecast
        forecast_timestamps = []
        forecast_values = []
        
        # Use historical data as context
        context = historical_counts.copy()
        
        for i in range(hours_ahead):
            forecast_time = start_timestamp + timedelta(hours=i)
            
            # Prepare features
            features = self._prepare_features(forecast_time, context)
            
            # Create sequence (need last 48 hours)
            if len(context) < self.seq_length:
                # Pad with last value
                padded_context = context + [context[-1]] * (self.seq_length - len(context))
            else:
                padded_context = context[-self.seq_length:]
            
            # Prepare sequence features
            seq_features = []
            for j in range(self.seq_length):
                seq_time = forecast_time - timedelta(hours=self.seq_length - j)
                seq_features.append(self._prepare_features(seq_time, context)[0])
            
            seq_features = np.array(seq_features).reshape(1, self.seq_length, 5)
            
            # Predict
            with torch.no_grad():
                x_tensor = torch.tensor(seq_features, dtype=torch.float32).to(self.device)
                pred = self.model(x_tensor).cpu().numpy()[0, 0]
                
                # Inverse transform
                dummy_pred = np.zeros((1, 3))
                dummy_pred[0, 0] = pred
                pred_inv = self.target_scaler.inverse_transform(dummy_pred)[0, 0]
                pred_inv = max(0, pred_inv)  # Ensure non-negative
            
            forecast_timestamps.append(forecast_time.isoformat())
            forecast_values.append(float(pred_inv))
            
            # Update context for next prediction
            context.append(pred_inv)
        
        return {
            'forecast': [
                {
                    'timestamp': ts,
                    'predicted_load': val
                }
                for ts, val in zip(forecast_timestamps, forecast_values)
            ],
            'hours_ahead': hours_ahead,
            'start_timestamp': start_timestamp.isoformat()
        }
