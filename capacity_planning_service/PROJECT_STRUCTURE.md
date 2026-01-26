# Project Structure

Overview of the Infrastructure Capacity Planning Microservice structure.

```
capacity_planning_service/
│
├── app.py                          # Main Flask application
├── model_service.py                # Model loading and prediction service
├── capacity_planner.py             # Capacity planning logic
│
├── templates/
│   └── index.html                  # Frontend dashboard (HTML/CSS/JS)
│
├── models/                         # Model files directory
│   ├── .gitkeep                    # Placeholder for model files
│   ├── attention_lstm.pth          # Trained model weights (add after training)
│   ├── target_scaler.pkl           # Target scaler (add after training)
│   └── time_scaler.pkl             # Time feature scaler (add after training)
│
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
│
└── Documentation/
    ├── README.md                   # Main documentation
    ├── API_DOCUMENTATION.md        # Complete API reference
    ├── SETUP.md                    # Detailed setup guide
    ├── QUICK_START.md              # Quick start guide
    └── PROJECT_STRUCTURE.md        # This file
```

## File Descriptions

### Core Application Files

#### `app.py`
- Main Flask application
- Defines all API endpoints
- Handles HTTP requests and responses
- Integrates model service and capacity planner
- Serves the frontend dashboard

#### `model_service.py`
- Loads the trained Attention LSTM model
- Handles model inference
- Prepares features for prediction
- Manages scalers (target and time)
- Generates forecasts

#### `capacity_planner.py`
- Implements capacity planning logic
- Generates scaling recommendations
- Performs risk assessment
- Creates multiple scaling scenarios
- Analyzes utilization patterns

### Frontend

#### `templates/index.html`
- Modern, responsive web dashboard
- Interactive charts using Chart.js
- Real-time forecast visualization
- Capacity metrics display
- Recommendation cards
- Form controls for API parameters

### Configuration

#### `requirements.txt`
- Python package dependencies
- Version-pinned for stability
- Includes: Flask, PyTorch, NumPy, Pandas, scikit-learn, etc.

#### `.gitignore`
- Excludes model files (too large for git)
- Excludes Python cache files
- Excludes IDE and OS files

### Documentation

#### `README.md`
- Complete project overview
- Features and capabilities
- Quick start instructions
- API documentation summary
- Architecture overview
- Troubleshooting guide

#### `API_DOCUMENTATION.md`
- Detailed API endpoint documentation
- Request/response examples
- Status codes
- Error handling
- Integration examples (Python, JavaScript)

#### `SETUP.md`
- Step-by-step setup instructions
- Prerequisites checklist
- Virtual environment setup
- Model file preparation
- Troubleshooting section
- Production deployment tips

#### `QUICK_START.md`
- 5-minute quick start guide
- Essential commands
- Basic API tests
- Dashboard usage

## Data Flow

```
User Request
    ↓
Flask App (app.py)
    ↓
Model Service (model_service.py)
    ├── Load model
    ├── Prepare features
    └── Generate forecast
    ↓
Capacity Planner (capacity_planner.py)
    ├── Analyze forecast
    ├── Calculate recommendations
    └── Assess risks
    ↓
Response (JSON)
    ↓
Frontend (index.html)
    ├── Display charts
    ├── Show metrics
    └── Render recommendations
```

## API Endpoints

1. `GET /` - Dashboard (HTML)
2. `GET /api/health` - Health check
3. `POST /api/forecast` - Get forecast
4. `POST /api/capacity/recommendations` - Get recommendations
5. `POST /api/capacity/analyze` - Comprehensive analysis

## Model Architecture

- **Type**: Attention-based Bidirectional LSTM
- **Input Features**: 5 (transaction_count, lag_24, lag_168, hour, dayofweek)
- **Sequence Length**: 48 hours
- **Hidden Size**: 128
- **Layers**: 2 bidirectional LSTM layers
- **Output**: Single value (predicted transaction count)

## Dependencies

### Core
- Flask 3.0.0 - Web framework
- PyTorch 2.1.0 - Deep learning
- NumPy 1.24.3 - Numerical computing
- Pandas 2.0.3 - Data manipulation
- scikit-learn 1.3.0 - Machine learning utilities

### Supporting
- flask-cors 4.0.0 - CORS support
- joblib 1.3.2 - Model serialization
- pyarrow 14.0.1 - ORC file support (if needed)

## Frontend Dependencies

Loaded via CDN:
- Chart.js 4.4.0 - Charting library

## Development Workflow

1. **Development**:
   ```bash
   python app.py  # Runs in debug mode
   ```

2. **Testing**:
   - Use curl or Postman for API testing
   - Use browser for dashboard testing
   - Check health endpoint first

3. **Production**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

## Model Training Workflow

1. Train model in Jupyter notebook
2. Save model files (attention_lstm.pth, scalers)
3. Copy files to `models/` directory
4. Service automatically loads on startup

## Extension Points

### Adding New Features

1. **New API Endpoint**: Add to `app.py`
2. **New Planning Logic**: Extend `capacity_planner.py`
3. **New Model**: Modify `model_service.py`
4. **Frontend Feature**: Update `templates/index.html`

### Integration Points

- Database: Add database connection in `app.py`
- Authentication: Add middleware in `app.py`
- Monitoring: Add logging/metrics collection
- Auto-scaling: Integrate with cloud APIs (AWS, GCP, Azure)

## Security Considerations

- Input validation (add in `app.py`)
- Authentication (add middleware)
- Rate limiting (add Flask-Limiter)
- HTTPS (use reverse proxy)
- Error sanitization (don't expose internals)

## Performance Optimization

- Model caching (already implemented)
- Response caching (add Redis)
- Async requests (use Flask async or FastAPI)
- Batch predictions (extend API)
- GPU acceleration (automatic if available)

---

**Last Updated**: 2024-01-15
