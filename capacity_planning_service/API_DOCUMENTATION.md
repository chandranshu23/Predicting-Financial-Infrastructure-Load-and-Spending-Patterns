# API Documentation

Complete API reference for the Infrastructure Capacity Planning Microservice.

## Base URL

```
http://localhost:5000
```

## Endpoints

### 1. Health Check

Check service status and model availability.

**Endpoint:** `GET /api/health`

**Parameters:** None

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2024-01-15T10:00:00.123456"
}
```

**Status Codes:**
- `200 OK`: Service is running

**Example:**
```bash
curl http://localhost:5000/api/health
```

---

### 2. Get Forecast

Generate load forecast for the next N hours.

**Endpoint:** `POST /api/forecast`

**Request Body:**
```json
{
  "hours_ahead": 24,              // Optional, default: 24, range: 1-168
  "current_load": 1000,           // Optional, current transaction count
  "timestamp": "2024-01-15T10:00:00"  // Optional, defaults to now
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
    {
      "timestamp": "2024-01-15T12:00:00",
      "predicted_load": 1380.2
    }
    // ... more forecast points
  ],
  "hours_ahead": 24,
  "start_timestamp": "2024-01-15T10:00:00"
}
```

**Status Codes:**
- `200 OK`: Forecast generated successfully
- `500 Internal Server Error`: Model not loaded or prediction error

**Example:**
```bash
curl -X POST http://localhost:5000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{
    "hours_ahead": 24,
    "current_load": 1000
  }'
```

**Python Example:**
```python
import requests

response = requests.post('http://localhost:5000/api/forecast', json={
    'hours_ahead': 24,
    'current_load': 1000
})
data = response.json()
print(data['forecast'])
```

---

### 3. Get Capacity Recommendations

Get scaling recommendations based on forecasted load.

**Endpoint:** `POST /api/capacity/recommendations`

**Request Body:**
```json
{
  "hours_ahead": 24,              // Optional, default: 24
  "current_capacity": 5000,       // Required, max transactions/hour
  "current_load": 1000,           // Optional, current transaction count
  "scaling_threshold": 0.8        // Optional, default: 0.8 (80%)
}
```

**Response:**
```json
{
  "success": true,
  "forecast": {
    "forecast": [ ... ],
    "hours_ahead": 24,
    "start_timestamp": "2024-01-15T10:00:00"
  },
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
    "peak_hours": [
      {
        "timestamp": "2024-01-15T14:00:00",
        "predicted_load": 5150.5
      }
    ],
    "message": "⚠️ Scale UP required: Increase capacity by 1,500 (30.0%) to 6,500. Current utilization will reach 104.0%."
  }
}
```

**Action Types:**
- `scale_up`: Increase capacity (utilization >= threshold)
- `scale_down`: Decrease capacity (utilization < 30%)
- `maintain`: Keep current capacity

**Urgency Levels:**
- `high`: Critical capacity issues
- `medium`: Capacity concerns
- `low`: Normal operations

**Status Codes:**
- `200 OK`: Recommendations generated successfully
- `500 Internal Server Error`: Error generating recommendations

**Example:**
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

---

### 4. Comprehensive Analysis

Get detailed capacity analysis with multiple scenarios.

**Endpoint:** `POST /api/capacity/analyze`

**Request Body:**
```json
{
  "hours_ahead": 168,             // Optional, default: 168 (1 week)
  "current_capacity": 5000,       // Required
  "current_load": 1000,           // Optional
  "scaling_threshold": 0.8        // Optional, default: 0.8
}
```

**Response:**
```json
{
  "success": true,
  "forecast": { ... },
  "analysis": {
    "summary": {
      "forecast_period_hours": 168,
      "current_capacity": 5000,
      "scaling_threshold": 0.8
    },
    "load_statistics": {
      "max_load": 5200,
      "min_load": 800,
      "avg_load": 2500,
      "std_load": 1200
    },
    "utilization_statistics": {
      "max_utilization": 1.04,
      "avg_utilization": 0.5,
      "min_utilization": 0.16
    },
    "risk_assessment": {
      "over_capacity_hours": 12,
      "critical_hours": 5,
      "under_utilized_hours": 45,
      "risk_level": "medium"
    },
    "hourly_patterns": {
      "peak_hour": 14,
      "low_hour": 3,
      "avg_load_by_hour": {
        "0": 1200,
        "1": 1100,
        ...
      }
    },
    "recommendations": { ... },
    "scaling_scenarios": {
      "conservative": {
        "capacity": 7800,
        "description": "20% buffer above peak load",
        "cost_impact": "high"
      },
      "balanced": {
        "capacity": 7150,
        "description": "10% buffer above peak load",
        "cost_impact": "medium"
      },
      "aggressive": {
        "capacity": 6500,
        "description": "Exact capacity for peak load",
        "cost_impact": "low"
      },
      "average_based": {
        "capacity": 4687,
        "description": "Capacity based on average load",
        "cost_impact": "low"
      }
    }
  }
}
```

**Risk Levels:**
- `critical`: >10% of hours are critical
- `high`: >20% of hours over capacity
- `medium`: >5% of hours over capacity
- `low`: <5% of hours over capacity

**Status Codes:**
- `200 OK`: Analysis generated successfully
- `500 Internal Server Error`: Error generating analysis

**Example:**
```bash
curl -X POST http://localhost:5000/api/capacity/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "hours_ahead": 168,
    "current_capacity": 5000,
    "current_load": 1000,
    "scaling_threshold": 0.8
  }'
```

---

## Error Responses

All endpoints may return error responses:

```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

**Common Error Messages:**
- `"Model not loaded. Please ensure model files exist."`
- `"No forecast data provided"`
- `"Invalid input parameters"`

---

## Rate Limiting

Currently, there is no rate limiting implemented. For production deployments, consider adding:
- Request throttling
- API key authentication
- Rate limit headers

---

## Best Practices

1. **Check Health First**: Always check `/api/health` before making predictions
2. **Handle Errors**: Always check `success` field in responses
3. **Use Appropriate Timeframes**: 
   - Short-term: 24-48 hours
   - Medium-term: 168 hours (1 week)
   - Long-term: Not recommended (accuracy decreases)
4. **Update Current Load**: Provide accurate `current_load` for better predictions
5. **Monitor Recommendations**: Track recommendation changes over time

---

## Integration Examples

### Python Integration

```python
import requests
import time

class CapacityPlanningClient:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
    
    def health_check(self):
        response = requests.get(f'{self.base_url}/api/health')
        return response.json()
    
    def get_forecast(self, hours_ahead=24, current_load=None):
        payload = {'hours_ahead': hours_ahead}
        if current_load:
            payload['current_load'] = current_load
        
        response = requests.post(
            f'{self.base_url}/api/forecast',
            json=payload
        )
        return response.json()
    
    def get_recommendations(self, current_capacity, hours_ahead=24, 
                           current_load=None, scaling_threshold=0.8):
        payload = {
            'current_capacity': current_capacity,
            'hours_ahead': hours_ahead,
            'scaling_threshold': scaling_threshold
        }
        if current_load:
            payload['current_load'] = current_load
        
        response = requests.post(
            f'{self.base_url}/api/capacity/recommendations',
            json=payload
        )
        return response.json()

# Usage
client = CapacityPlanningClient()
health = client.health_check()
if health['model_loaded']:
    forecast = client.get_forecast(hours_ahead=24, current_load=1000)
    recommendations = client.get_recommendations(
        current_capacity=5000,
        hours_ahead=24,
        current_load=1000
    )
```

### JavaScript/Node.js Integration

```javascript
const axios = require('axios');

class CapacityPlanningClient {
    constructor(baseUrl = 'http://localhost:5000') {
        this.baseUrl = baseUrl;
    }
    
    async healthCheck() {
        const response = await axios.get(`${this.baseUrl}/api/health`);
        return response.data;
    }
    
    async getForecast(hoursAhead = 24, currentLoad = null) {
        const payload = { hours_ahead: hoursAhead };
        if (currentLoad) payload.current_load = currentLoad;
        
        const response = await axios.post(
            `${this.baseUrl}/api/forecast`,
            payload
        );
        return response.data;
    }
    
    async getRecommendations(currentCapacity, hoursAhead = 24, 
                            currentLoad = null, scalingThreshold = 0.8) {
        const payload = {
            current_capacity: currentCapacity,
            hours_ahead: hoursAhead,
            scaling_threshold: scalingThreshold
        };
        if (currentLoad) payload.current_load = currentLoad;
        
        const response = await axios.post(
            `${this.base_url}/api/capacity/recommendations`,
            payload
        );
        return response.data;
    }
}

// Usage
const client = new CapacityPlanningClient();
const health = await client.healthCheck();
if (health.model_loaded) {
    const forecast = await client.getForecast(24, 1000);
    const recommendations = await client.getRecommendations(5000, 24, 1000);
}
```

---

## Version

Current API Version: **1.0.0**

For updates and changes, check the main README.md file.
