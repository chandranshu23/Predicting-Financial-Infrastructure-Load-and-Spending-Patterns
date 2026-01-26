# Infrastructure Capacity Planning Microservice

A Flask-based microservice for AI-powered infrastructure capacity planning using financial load forecasting. This service provides real-time load predictions and automated scaling recommendations to optimize infrastructure resources.

## 🎯 Features

- **AI-Powered Forecasting**: Uses Attention-based LSTM model to predict transaction loads
- **Capacity Recommendations**: Automated scaling recommendations based on forecasted load
- **Risk Assessment**: Comprehensive analysis of capacity risks and utilization patterns
- **Interactive Dashboard**: Modern web interface with real-time charts and metrics
- **RESTful API**: Well-documented API endpoints for integration
- **Multiple Scenarios**: Compare different scaling strategies (conservative, balanced, aggressive)

## 📋 Prerequisites

- Python 3.8 or higher
- PyTorch (CPU or CUDA-enabled)
- Model files from training:
  - `attention_lstm.pth` (trained model weights)
  - `target_scaler.pkl` (target scaler)
  - `time_scaler.pkl` (time feature scaler)

## 🚀 Quick Start

### 1. Setup Environment

**Important**: On macOS, you must use a virtual environment due to externally-managed Python restrictions.

**Option 1: Using Setup Script (Recommended)**
```bash
./setup.sh
source venv/bin/activate
```

**Option 2: Manual Setup**
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Prepare Model Files

Ensure you have the trained model files in the `models/` directory:

```
capacity_planning_service/
├── models/
│   ├── attention_lstm.pth
│   ├── target_scaler.pkl
│   └── time_scaler.pkl
├── app.py
├── model_service.py
├── capacity_planner.py
└── requirements.txt
```

**Note**: If you haven't trained the model yet, run the training notebook (`Model_training_financial_load_forecasting.ipynb`) and save the model files to the `models/` directory.

### 3. Run the Service

```bash
python app.py
```

The service will start on `http://localhost:5000`

### 4. Access the Dashboard

Open your browser and navigate to:
```
http://localhost:5000
```

## 📚 API Documentation

### Health Check

**GET** `/api/health`

Check if the service is running and model is loaded.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2024-01-15T10:00:00"
}
```

### Get Forecast

**POST** `/api/forecast`

Generate load forecast for the next N hours.

**Request Body:**
```json
{
  "hours_ahead": 24,
  "current_load": 1000,
  "timestamp": "2024-01-15T10:00:00"
}
```

**Response:**
```json
{
  "success": true,
  "forecast": [
    {
      "timestamp": "2024-01-15T11:00:00",
      "predicted_load": 1250.5
    },
    ...
  ],
  "timestamp": "2024-01-15T10:00:00"
}
```

### Get Capacity Recommendations

**POST** `/api/capacity/recommendations`

Get scaling recommendations based on forecast.

**Request Body:**
```json
{
  "hours_ahead": 24,
  "current_capacity": 5000,
  "current_load": 1000,
  "scaling_threshold": 0.8
}
```

**Response:**
```json
{
  "success": true,
  "forecast": { ... },
  "recommendations": {
    "action": "scale_up",
    "urgency": "high",
    "current_capacity": 5000,
    "recommended_capacity": 6500,
    "capacity_change": 1500,
    "capacity_change_percent": 30.0,
    "metrics": {
      "max_predicted_load": 5200,
      "avg_predicted_load": 3500,
      "min_predicted_load": 1200,
      "max_utilization": 1.04,
      "avg_utilization": 0.7
    },
    "peak_hours": [ ... ],
    "message": "⚠️ Scale UP required..."
  }
}
```

### Comprehensive Analysis

**POST** `/api/capacity/analyze`

Get comprehensive capacity analysis with multiple scenarios.

**Request Body:**
```json
{
  "hours_ahead": 168,
  "current_capacity": 5000,
  "current_load": 1000,
  "scaling_threshold": 0.8
}
```

**Response:**
```json
{
  "success": true,
  "forecast": { ... },
  "analysis": {
    "summary": { ... },
    "load_statistics": { ... },
    "utilization_statistics": { ... },
    "risk_assessment": {
      "risk_level": "medium",
      "critical_hours": 5,
      "over_capacity_hours": 12,
      "under_utilized_hours": 45
    },
    "hourly_patterns": { ... },
    "recommendations": { ... },
    "scaling_scenarios": {
      "conservative": { ... },
      "balanced": { ... },
      "aggressive": { ... },
      "average_based": { ... }
    }
  }
}
```

## 🏗️ Architecture

### Components

1. **app.py**: Flask application with API endpoints
2. **model_service.py**: Model loading and prediction service
3. **capacity_planner.py**: Capacity planning logic and recommendations
4. **templates/index.html**: Frontend dashboard

### Model Architecture

The service uses an **Attention-based Bidirectional LSTM** model:
- **Input Features**: 5 features (transaction_count, lag_24, lag_168, hour, dayofweek)
- **Sequence Length**: 48 hours (2 days of historical context)
- **Hidden Size**: 128
- **Layers**: 2 bidirectional LSTM layers with attention mechanism

### Capacity Planning Logic

The service provides recommendations based on:
- **Scaling Threshold**: Default 80% utilization triggers scaling
- **Peak Detection**: Identifies hours with highest predicted load
- **Risk Assessment**: Categorizes risk levels (low, medium, high, critical)
- **Multiple Scenarios**: Provides different scaling strategies

## 🔧 Configuration

### Environment Variables

You can configure the service using environment variables:

```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
export PORT=5000
export MODEL_DIR=models
```

### Scaling Threshold

Adjust the scaling threshold based on your infrastructure:
- **Conservative (0.7)**: Scale earlier, more headroom
- **Balanced (0.8)**: Default, good balance
- **Aggressive (0.9)**: Scale later, cost-optimized

## 📊 Usage Examples

### Python Client

```python
import requests

# Get forecast
response = requests.post('http://localhost:5000/api/forecast', json={
    'hours_ahead': 24,
    'current_load': 1000
})
forecast = response.json()

# Get recommendations
response = requests.post('http://localhost:5000/api/capacity/recommendations', json={
    'hours_ahead': 24,
    'current_capacity': 5000,
    'current_load': 1000,
    'scaling_threshold': 0.8
})
recommendations = response.json()
```

### cURL

```bash
# Health check
curl http://localhost:5000/api/health

# Get forecast
curl -X POST http://localhost:5000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"hours_ahead": 24, "current_load": 1000}'

# Get recommendations
curl -X POST http://localhost:5000/api/capacity/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "hours_ahead": 24,
    "current_capacity": 5000,
    "current_load": 1000,
    "scaling_threshold": 0.8
  }'
```

## 🐳 Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

Build and run:

```bash
docker build -t capacity-planning-service .
docker run -p 5000:5000 capacity-planning-service
```

## 🔍 Monitoring & Logging

The service logs important events:
- Model loading status
- API requests
- Prediction errors
- Capacity recommendations

For production, consider integrating with:
- **Logging**: Python logging module
- **Monitoring**: Prometheus, Grafana
- **Alerting**: PagerDuty, Slack webhooks

## 🚨 Troubleshooting

### Model Not Loading

**Issue**: `model_loaded: false` in health check

**Solutions**:
1. Ensure model files exist in `models/` directory
2. Check file permissions
3. Verify model files are from the same training run

### CUDA Out of Memory

**Issue**: GPU memory errors

**Solutions**:
1. Use CPU mode: The service automatically falls back to CPU
2. Reduce batch size in model_service.py
3. Clear GPU cache: `torch.cuda.empty_cache()`

### Forecast Accuracy

**Issue**: Predictions seem inaccurate

**Solutions**:
1. Ensure historical data is recent and relevant
2. Check if current_load parameter is accurate
3. Verify model was trained on similar data patterns

## 📈 Performance

- **Prediction Time**: ~50-100ms per forecast (CPU), ~10-20ms (GPU)
- **Throughput**: ~100-200 requests/second (depending on hardware)
- **Memory Usage**: ~500MB-1GB (model + dependencies)

## 🔐 Security Considerations

For production deployment:

1. **Authentication**: Add API key or OAuth2
2. **Rate Limiting**: Implement request throttling
3. **HTTPS**: Use SSL/TLS certificates
4. **Input Validation**: Validate all API inputs
5. **Error Handling**: Don't expose internal errors

## 📝 License

This project is part of the Financial Infrastructure Load Forecasting system.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation
3. Check model training notebook for model details

---

**Built with ❤️ using Flask, PyTorch, and Chart.js**
