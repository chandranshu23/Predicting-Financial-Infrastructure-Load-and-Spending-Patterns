"""
Flask Microservice for Infrastructure Capacity Planning
Based on Financial Load Forecasting Model
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import pandas as pd
import joblib
import os
from datetime import datetime, timedelta
from model_service import ModelService
from capacity_planner import CapacityPlanner

app = Flask(__name__)
CORS(app)

# Initialize services
model_service = ModelService()
capacity_planner = CapacityPlanner()

@app.route('/')
def index():
    """Serve the frontend dashboard"""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_service.is_loaded(),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/capacity/recommendations', methods=['POST'])
def get_capacity_recommendations():
    """
    Get capacity planning recommendations based on forecast
    
    Request body:
    {
        "hours_ahead": 24,
        "current_capacity": 5000,  # Current max transactions per hour
        "current_load": 1000,
        "scaling_threshold": 0.8  # Optional, default 0.8 (80%)
    }
    """
    try:
        data = request.get_json() or {}
        hours_ahead = data.get('hours_ahead', 24)
        current_capacity = data.get('current_capacity', 5000)
        current_load = data.get('current_load', None)
        scaling_threshold = data.get('scaling_threshold', 0.8)
        
        # Get forecast
        forecast_result = model_service.forecast(
            hours_ahead=hours_ahead,
            current_load=current_load
        )
        
        # Get recommendations
        recommendations = capacity_planner.get_recommendations(
            forecast=forecast_result['forecast'],
            current_capacity=current_capacity,
            scaling_threshold=scaling_threshold
        )
        
        return jsonify({
            'success': True,
            'forecast': forecast_result,
            'recommendations': recommendations
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Capacity Planning Service...")
    print(f"📊 Model loaded: {model_service.is_loaded()}")
    app.run(debug=True, host='0.0.0.0', port=5002)
