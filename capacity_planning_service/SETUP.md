# Setup Guide

Step-by-step guide to set up and run the Infrastructure Capacity Planning Microservice.

## Prerequisites Checklist

- [ ] Python 3.8 or higher installed
- [ ] pip package manager available
- [ ] Trained model files (or access to training notebook)
- [ ] At least 2GB free disk space
- [ ] Internet connection (for downloading dependencies)

## Step 1: Verify Python Installation

```bash
python --version
# Should show Python 3.8 or higher

pip --version
# Should show pip version
```

## Step 2: Create Virtual Environment (Recommended)

**Important**: On macOS with Homebrew Python, you **must** use a virtual environment due to externally-managed environment restrictions.

### Option 1: Using Setup Script (Easiest)

```bash
# Navigate to the service directory
cd capacity_planning_service

# Run the setup script
./setup.sh
```

The script will automatically:
- Create a virtual environment
- Install all dependencies
- Set everything up for you

### Option 2: Manual Setup

```bash
# Navigate to the service directory
cd capacity_planning_service

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

## Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note**: PyTorch installation may take a few minutes. If you have CUDA-enabled GPU, you may want to install PyTorch with CUDA support separately:

```bash
# For CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Then install other dependencies
pip install -r requirements.txt
```

## Step 4: Prepare Model Files

You have two options:

### Option A: Use Existing Model Files

If you've already trained the model, copy the files to the `models/` directory:

```bash
# From the directory where you saved the model
cp attention_lstm.pth capacity_planning_service/models/
cp target_scaler.pkl capacity_planning_service/models/
cp time_scaler.pkl capacity_planning_service/models/
```

### Option B: Train the Model First

1. Open the Jupyter notebook: `sparkScripts/Model_training_financial_load_forecasting.ipynb`
2. Run all cells, especially the "Best model" section (Cell 9)
3. The model files will be saved in the current directory
4. Copy them to `capacity_planning_service/models/`:

```bash
cp attention_lstm.pth capacity_planning_service/models/
cp target_scaler.pkl capacity_planning_service/models/
cp time_scaler.pkl capacity_planning_service/models/
```

## Step 5: Verify Model Files

```bash
ls -lh capacity_planning_service/models/
# Should show:
# - attention_lstm.pth (model weights, typically 5-10 MB)
# - target_scaler.pkl (scaler file, typically < 1 MB)
# - time_scaler.pkl (scaler file, typically < 1 MB)
```

## Step 6: Test the Service

```bash
# Start the service
python app.py
```

You should see:
```
🚀 Starting Capacity Planning Service...
✅ Model loaded successfully on cpu (or cuda)
📊 Model loaded: True
 * Running on http://0.0.0.0:5000
```

## Step 7: Access the Dashboard

Open your web browser and navigate to:
```
http://localhost:5000
```

You should see the Infrastructure Capacity Planning Dashboard.

## Step 8: Test API Endpoints

### Test Health Check

```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2024-01-15T10:00:00"
}
```

### Test Forecast

```bash
curl -X POST http://localhost:5000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"hours_ahead": 24, "current_load": 1000}'
```

## Troubleshooting

### Issue: "Model not loaded"

**Symptoms**: Health check shows `"model_loaded": false`

**Solutions**:
1. Check if model files exist:
   ```bash
   ls -la capacity_planning_service/models/
   ```
2. Verify file permissions:
   ```bash
   chmod 644 capacity_planning_service/models/*.pth
   chmod 644 capacity_planning_service/models/*.pkl
   ```
3. Check file paths in `model_service.py` (should be `models/`)

### Issue: Import Errors

**Symptoms**: `ModuleNotFoundError` or `ImportError`

**Solutions**:
1. Ensure virtual environment is activated
2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```
3. Check Python version:
   ```bash
   python --version  # Should be 3.8+
   ```

### Issue: CUDA/GPU Errors

**Symptoms**: CUDA-related errors even with GPU available

**Solutions**:
1. The service automatically falls back to CPU - this is fine
2. If you want GPU support, ensure:
   - NVIDIA drivers are installed
   - CUDA toolkit is installed
   - PyTorch with CUDA is installed:
     ```bash
     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
     ```

### Issue: Port Already in Use

**Symptoms**: `Address already in use` error

**Solutions**:
1. Find and kill the process using port 5000:
   ```bash
   # macOS/Linux
   lsof -ti:5000 | xargs kill -9
   
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   ```
2. Or change the port in `app.py`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

### Issue: Forecast Returns Zero or Negative Values

**Symptoms**: Predictions are 0 or negative

**Solutions**:
1. This is normal for synthetic historical data
2. In production, use real historical data
3. The model uses `max(0, pred_inv)` to ensure non-negative values

## Production Deployment

For production deployment, consider:

1. **Use a Production WSGI Server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Set Environment Variables**:
   ```bash
   export FLASK_ENV=production
   export FLASK_DEBUG=False
   ```

3. **Use a Reverse Proxy** (nginx, Apache)

4. **Add Authentication** (API keys, OAuth2)

5. **Enable Logging**:
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```

6. **Monitor Resources**:
   - CPU usage
   - Memory usage
   - Response times
   - Error rates

## Next Steps

1. ✅ Service is running
2. ✅ Dashboard is accessible
3. ✅ API endpoints are working
4. 📖 Read [README.md](README.md) for detailed documentation
5. 📖 Read [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API reference
6. 🚀 Start integrating with your infrastructure!

## Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review error messages in the terminal
3. Check the health endpoint: `curl http://localhost:5000/api/health`
4. Verify model files are correct
5. Check Python and package versions

---

**Setup Complete!** 🎉

You're ready to use the Infrastructure Capacity Planning Microservice.
