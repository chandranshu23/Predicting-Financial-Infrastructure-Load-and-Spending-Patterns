# Quick Start Guide

Get up and running in 5 minutes!

## 🚀 Quick Setup

### Option 1: Using Setup Script (Recommended)

```bash
# Run the setup script
./setup.sh

# Activate virtual environment (if not already activated)
source venv/bin/activate

# Run the service
python app.py
```

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Ensure model files are in models/ directory
# (Copy from training notebook output or existing location)

# 5. Run the service
python app.py

# 6. Open browser
# http://localhost:5000
```

## 📋 Prerequisites

- Python 3.8+
- Model files: `attention_lstm.pth`, `target_scaler.pkl`, `time_scaler.pkl`

## 🎯 Quick Test

### 1. Check Health
```bash
curl http://localhost:5000/api/health
```

### 2. Get Forecast
```bash
curl -X POST http://localhost:5000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"hours_ahead": 24, "current_load": 1000}'
```

### 3. Get Recommendations
```bash
curl -X POST http://localhost:5000/api/capacity/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "hours_ahead": 24,
    "current_capacity": 5000,
    "current_load": 1000,
    "scaling_threshold": 0.8
  }'
```

## 🖥️ Using the Dashboard

1. Open `http://localhost:5000` in your browser
2. Set your parameters:
   - Forecast Hours: 24
   - Current Capacity: 5000
   - Current Load: 1000
   - Scaling Threshold: 80%
3. Click "Get Recommendations"
4. View forecast chart and recommendations

## 📚 Next Steps

- Read [README.md](README.md) for full documentation
- Read [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details
- Read [SETUP.md](SETUP.md) for detailed setup instructions

## ⚠️ Troubleshooting

**Model not loading?**
- Check `models/` directory has all 3 files
- Verify file permissions

**Port in use?**
- Change port in `app.py`: `app.run(port=5001)`

**Import errors?**
- Activate virtual environment
- Run: `pip install -r requirements.txt`

---

**That's it!** You're ready to use the service. 🎉
