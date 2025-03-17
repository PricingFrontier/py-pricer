#!/bin/bash

# Display banner
echo "=========================================================="
echo "            PY-PRICER LOCAL ENVIRONMENT SETUP            "
echo "=========================================================="
echo "This script will set up your local development environment"
echo ""

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "🔄 UV package manager not found. Installing now..."
    pip install uv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install UV. Please install manually: pip install uv"
        exit 1
    fi
    echo "✅ UV installed successfully!"
else
    echo "✅ UV already installed!"
fi

echo ""
echo "🔄 Creating a virtual environment..."
uv venv
echo "✅ Virtual environment created!"

echo ""
echo "🔄 Installing dependencies from pyproject.toml..."
# Use pyproject.toml as the source for uv pip sync
uv pip sync pyproject.toml
echo "✅ Dependencies installed!"

echo ""
echo "🔄 Setting up pre-commit hooks..."
if ! command -v pre-commit &> /dev/null; then
    uv pip install pre-commit
    echo "✅ pre-commit installed!"
else
    echo "✅ pre-commit already installed!"
fi

if [ -f ".pre-commit-config.yaml" ]; then
    pre-commit install
    echo "✅ Pre-commit hooks installed!"
else
    echo "ℹ️ No .pre-commit-config.yaml found, skipping pre-commit setup."
fi

echo ""
echo "🎉 LOCAL ENVIRONMENT SETUP COMPLETE! 🎉"
echo "==========================================="
echo "To activate your virtual environment:"
echo "  source .venv/bin/activate  # On Linux/macOS"
echo "  .venv\\Scripts\\activate     # On Windows"
echo ""
echo "To run the API locally:"
echo "  python -m py_pricer.api_launcher"
echo "  # or use the command: pypricer-api"
echo ""
echo "To run the UI locally:"
echo "  python -m py_pricer.app_launcher"
echo "  # or use the command: pypricer-ui"
echo ""
echo "To run tests:"
echo "  python -m pytest"
echo "===========================================" 