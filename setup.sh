#!/bin/bash

# Anomaly Detection Agent - Setup Script with UV
echo "🔧 Setting up Anomaly Detection Agent..."
echo ""

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed!"
    echo "Please install UV first: https://github.com/astral-sh/uv"
    echo ""
    echo "Quick install:"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Create virtual environment with UV
if [ ! -d ".venv" ]; then
    echo "📦 Creating UV virtual environment..."
    uv venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies with UV..."
uv pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Create a .env file with your OPENAI_API_KEY"
echo "   echo 'OPENAI_API_KEY=your_key_here' > .env"
echo ""
echo "2. Run the app:"
echo "   ./run.sh"
echo "   OR"
echo "   source .venv/bin/activate && streamlit run app.py"
echo ""
