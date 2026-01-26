#!/bin/bash

# Setup script for Infrastructure Capacity Planning Microservice
# This script creates a virtual environment and installs dependencies

set -e  # Exit on error

echo "🚀 Setting up Infrastructure Capacity Planning Microservice..."
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To start the service, run:"
echo "  python app.py"
echo ""
echo "⚠️  Don't forget to copy your model files to the models/ directory:"
echo "  - attention_lstm.pth"
echo "  - target_scaler.pkl"
echo "  - time_scaler.pkl"
