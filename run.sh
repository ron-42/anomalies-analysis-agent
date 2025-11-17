#!/bin/bash

# Anomaly Detection Agent - Streamlit Launcher
echo "🔍 Starting Anomaly Detection Agent with Streamlit UI..."
echo ""

# Activate UV virtual environment
if [ -d ".venv" ]; then
    echo "📦 Activating UV virtual environment..."
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  Warning: No virtual environment found (.venv or venv)"
    echo "Creating UV virtual environment..."
    uv venv
    source .venv/bin/activate
fi

echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create a .env file with your OPENAI_API_KEY"
    echo ""
    echo "Example:"
    echo "OPENAI_API_KEY=your_openai_api_key_here"
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit is not installed!"
    echo "Installing dependencies with UV..."
    uv pip install -r requirements.txt
fi

echo "🚀 Launching Streamlit app..."
echo ""
streamlit run app.py
