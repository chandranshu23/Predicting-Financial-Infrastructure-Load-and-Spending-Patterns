# How to Run the Service

Simple step-by-step guide to run the Infrastructure Capacity Planning Microservice.

## Prerequisites Check

Before running, ensure you have:
- ✅ Virtual environment created and dependencies installed
- ✅ Model files in `models/` directory (see below)

## Step-by-Step Instructions

### 1. Navigate to the Service Directory

```bash
cd capacity_planning_service
```

### 2. Activate Virtual Environment

```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 3. Check Model Files (Important!)

The service needs these files in the `models/` directory:
- `attention_lstm.pth` - Trained model weights
- `target_scaler.pkl` - Target scaler
- `time_scaler.pkl` - Time feature scaler

**If you don't have these files yet:**

1. Go to your training notebook: `sparkScripts/Model_training_financial_load_forecasting.ipynb`
2. Run the "Best model" section (Cell 9) which saves the model files
3. Copy the files to `models/` directory:
   ```bash
   cp attention_lstm.pth capacity_planning_service/models/
   cp target_scaler.pkl capacity_planning_service/models/
   cp time_scaler.pkl capacity_planning_service/models/
   ```

**Note**: The service will still start without model files, but predictions won't work. You'll see a warning in the health check.

### 4. Run the Service

```bash
python app.py
```

You should see output like:
```
🚀 Starting Capacity Planning Service...
✅ Model loaded successfully on cpu
📊 Model loaded: True
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### 5. Access the Dashboard

Open your web browser and go to:
```
http://localhost:5000
```

### 6. Test the API

Open a new terminal (keep the service running) and test:

```bash
# Health check
curl http://localhost:5000/api/health

# Get forecast
curl -X POST http://localhost:5000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"hours_ahead": 24, "current_load": 1000}'
```

## Quick Run Commands (All in One)

```bash
# Navigate to directory
cd capacity_planning_service

# Activate virtual environment
source venv/bin/activate

# Run the service
python app.py
```

## Using the Dashboard

1. **Set Parameters**:
   - Forecast Hours: 24 (or any number 1-168)
   - Current Capacity: 5000 (your max transactions/hour)
   - Current Load: 1000 (current transaction count)
   - Scaling Threshold: 80% (when to trigger scaling)

2. **Click Buttons**:
   - **Get Forecast**: Shows predicted load chart
   - **Get Recommendations**: Shows scaling recommendations
   - **Full Analysis**: Comprehensive analysis with scenarios

3. **View Results**:
   - Forecast chart (interactive)
   - Capacity metrics
   - Recommendations with action items
   - Risk assessment

## Stopping the Service

Press `Ctrl+C` in the terminal where the service is running.

## Troubleshooting

### "Model not loaded" Warning

**Problem**: Health check shows `"model_loaded": false`

**Solution**: 
1. Ensure model files are in `models/` directory
2. Check file permissions: `ls -la models/`
3. Verify files are from the same training run

### Port Already in Use

**Problem**: `Address already in use` error

**Solution**:
```bash
# Find and kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or change port in app.py
# app.run(debug=True, host='0.0.0.0', port=5001)
```

### Import Errors

**Problem**: `ModuleNotFoundError`

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Service Won't Start

**Problem**: Various startup errors

**Solution**:
1. Check Python version: `python --version` (should be 3.8+)
2. Verify virtual environment: `which python` (should show venv path)
3. Check all dependencies installed: `pip list`

## Production Mode

For production, use a WSGI server:

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Next Steps After Running

1. ✅ Service is running
2. ✅ Dashboard is accessible
3. ✅ Test API endpoints
4. 📊 Use the dashboard for capacity planning
5. 🔌 Integrate with your infrastructure

---

**That's it!** The service should now be running. 🚀
