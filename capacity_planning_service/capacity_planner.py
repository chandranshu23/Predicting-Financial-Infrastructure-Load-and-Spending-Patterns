"""
Capacity Planning Logic and Recommendations
"""

import numpy as np
from datetime import datetime, timedelta

class CapacityPlanner:
    """Service for generating capacity planning recommendations"""
    
    def __init__(self):
        self.scaling_factors = {
            'low': 0.5,      # Scale down to 50%
            'medium': 0.75,  # Scale down to 75%
            'high': 1.0,     # Maintain current
            'critical': 1.5  # Scale up to 150%
        }
    
    def get_recommendations(self, forecast, current_capacity, scaling_threshold=0.8):
        """
        Get capacity recommendations based on forecast
        
        Args:
            forecast: List of forecast dictionaries with 'timestamp' and 'predicted_load'
            current_capacity: Current maximum capacity (transactions/hour)
            scaling_threshold: Threshold for scaling (default 0.8 = 80%)
        
        Returns:
            Dictionary with recommendations
        """
        if not forecast:
            return {'error': 'No forecast data provided'}
        
        predicted_loads = [f['predicted_load'] for f in forecast]
        max_predicted = max(predicted_loads)
        avg_predicted = np.mean(predicted_loads)
        min_predicted = min(predicted_loads)
        
        # Calculate utilization
        max_utilization = max_predicted / current_capacity if current_capacity > 0 else 0
        avg_utilization = avg_predicted / current_capacity if current_capacity > 0 else 0
        
        # Determine action needed
        if max_utilization >= scaling_threshold:
            action = 'scale_up'
            urgency = 'high' if max_utilization >= 0.95 else 'medium'
            recommended_capacity = int(max_predicted / scaling_threshold * 1.1)  # 10% buffer
        elif avg_utilization < 0.3:
            action = 'scale_down'
            urgency = 'low'
            recommended_capacity = int(avg_predicted / scaling_threshold * 1.2)  # 20% buffer
        else:
            action = 'maintain'
            urgency = 'low'
            recommended_capacity = current_capacity
        
        # Find peak hours
        peak_hours = []
        for f in forecast:
            if f['predicted_load'] >= max_predicted * 0.9:  # Within 90% of max
                peak_hours.append({
                    'timestamp': f['timestamp'],
                    'predicted_load': f['predicted_load']
                })
        
        return {
            'action': action,
            'urgency': urgency,
            'current_capacity': current_capacity,
            'recommended_capacity': recommended_capacity,
            'capacity_change': recommended_capacity - current_capacity,
            'capacity_change_percent': ((recommended_capacity - current_capacity) / current_capacity * 100) if current_capacity > 0 else 0,
            'metrics': {
                'max_predicted_load': max_predicted,
                'avg_predicted_load': avg_predicted,
                'min_predicted_load': min_predicted,
                'max_utilization': max_utilization,
                'avg_utilization': avg_utilization
            },
            'peak_hours': peak_hours[:10],  # Top 10 peak hours
            'message': self._generate_message(action, urgency, max_utilization, recommended_capacity, current_capacity)
        }
    
    def analyze(self, forecast, current_capacity, scaling_threshold=0.8):
        """
        Comprehensive capacity analysis
        
        Args:
            forecast: List of forecast dictionaries
            current_capacity: Current maximum capacity
            scaling_threshold: Threshold for scaling
        
        Returns:
            Comprehensive analysis dictionary
        """
        if not forecast:
            return {'error': 'No forecast data provided'}
        
        predicted_loads = [f['predicted_load'] for f in forecast]
        timestamps = [f['timestamp'] for f in forecast]
        
        # Basic statistics
        max_load = max(predicted_loads)
        min_load = min(predicted_loads)
        avg_load = np.mean(predicted_loads)
        std_load = np.std(predicted_loads)
        
        # Utilization analysis
        utilizations = [load / current_capacity for load in predicted_loads]
        max_util = max(utilizations)
        avg_util = np.mean(utilizations)
        min_util = min(utilizations)
        
        # Risk assessment
        over_capacity_hours = sum(1 for u in utilizations if u >= scaling_threshold)
        critical_hours = sum(1 for u in utilizations if u >= 0.95)
        under_utilized_hours = sum(1 for u in utilizations if u < 0.3)
        
        # Time-based analysis
        hourly_patterns = {}
        for f in forecast:
            hour = datetime.fromisoformat(f['timestamp']).hour
            if hour not in hourly_patterns:
                hourly_patterns[hour] = []
            hourly_patterns[hour].append(f['predicted_load'])
        
        avg_by_hour = {hour: np.mean(loads) for hour, loads in hourly_patterns.items()}
        peak_hour = max(avg_by_hour.items(), key=lambda x: x[1])[0]
        low_hour = min(avg_by_hour.items(), key=lambda x: x[1])[0]
        
        # Recommendations
        recommendations = self.get_recommendations(forecast, current_capacity, scaling_threshold)
        
        return {
            'summary': {
                'forecast_period_hours': len(forecast),
                'current_capacity': current_capacity,
                'scaling_threshold': scaling_threshold
            },
            'load_statistics': {
                'max_load': max_load,
                'min_load': min_load,
                'avg_load': avg_load,
                'std_load': std_load
            },
            'utilization_statistics': {
                'max_utilization': max_util,
                'avg_utilization': avg_util,
                'min_utilization': min_util
            },
            'risk_assessment': {
                'over_capacity_hours': over_capacity_hours,
                'critical_hours': critical_hours,
                'under_utilized_hours': under_utilized_hours,
                'risk_level': self._assess_risk(critical_hours, over_capacity_hours, len(forecast))
            },
            'hourly_patterns': {
                'peak_hour': peak_hour,
                'low_hour': low_hour,
                'avg_load_by_hour': avg_by_hour
            },
            'recommendations': recommendations,
            'scaling_scenarios': self._generate_scenarios(forecast, current_capacity, scaling_threshold)
        }
    
    def _assess_risk(self, critical_hours, over_capacity_hours, total_hours):
        """Assess overall risk level"""
        critical_pct = critical_hours / total_hours if total_hours > 0 else 0
        over_capacity_pct = over_capacity_hours / total_hours if total_hours > 0 else 0
        
        if critical_pct > 0.1:  # More than 10% critical
            return 'critical'
        elif over_capacity_pct > 0.2:  # More than 20% over capacity
            return 'high'
        elif over_capacity_pct > 0.05:  # More than 5% over capacity
            return 'medium'
        else:
            return 'low'
    
    def _generate_scenarios(self, forecast, current_capacity, scaling_threshold):
        """Generate different scaling scenarios"""
        predicted_loads = [f['predicted_load'] for f in forecast]
        max_load = max(predicted_loads)
        avg_load = np.mean(predicted_loads)
        
        scenarios = {
            'conservative': {
                'capacity': int(max_load / scaling_threshold * 1.2),  # 20% buffer
                'description': '20% buffer above peak load',
                'cost_impact': 'high'
            },
            'balanced': {
                'capacity': int(max_load / scaling_threshold * 1.1),  # 10% buffer
                'description': '10% buffer above peak load',
                'cost_impact': 'medium'
            },
            'aggressive': {
                'capacity': int(max_load / scaling_threshold),  # No buffer
                'description': 'Exact capacity for peak load',
                'cost_impact': 'low'
            },
            'average_based': {
                'capacity': int(avg_load / scaling_threshold * 1.5),  # 50% above average
                'description': 'Capacity based on average load',
                'cost_impact': 'low'
            }
        }
        
        return scenarios
    
    def _generate_message(self, action, urgency, utilization, recommended, current):
        """Generate human-readable message"""
        if action == 'scale_up':
            change = recommended - current
            change_pct = (change / current * 100) if current > 0 else 0
            return f"⚠️ Scale UP required: Increase capacity by {change:,} ({change_pct:.1f}%) to {recommended:,}. Current utilization will reach {utilization*100:.1f}%."
        elif action == 'scale_down':
            change = current - recommended
            change_pct = (change / current * 100) if current > 0 else 0
            return f"✅ Scale DOWN recommended: Reduce capacity by {change:,} ({change_pct:.1f}%) to {recommended:,} to optimize costs."
        else:
            return f"✓ Maintain current capacity: {current:,} is adequate. Peak utilization: {utilization*100:.1f}%"
