#!/bin/bash

set -e

echo "🚀 Setting up Azure ML Playground environment..."

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt --user
else
    echo "⚠️  requirements.txt not found, skipping Python dependencies"
fi

# Install and configure nbstripout for notebooks
echo "🔧 Setting up nbstripout for Jupyter notebooks..."
pip install nbstripout
nbstripout --install --attributes .gitattributes

# Verify Azure CLI installation
if command -v az &> /dev/null; then
    echo "✅ Azure CLI is installed:"
    az version --output table 2>/dev/null || az version
else
    echo "❌ Azure CLI not found!"
    echo "Installing Azure CLI..."
    curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
fi

# Install Azure ML CLI extension
echo "🔧 Installing Azure ML CLI extension..."
if ! az extension add --name ml --yes 2>/dev/null; then
    echo "⚠️  Could not install Azure ML extension automatically (network issue or already installed)"
    echo "    You can install it manually later with: az extension add --name ml"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Run 'az login --use-device-code' to authenticate with Azure"
echo "2. Open notebooks/00_setup_connection.ipynb to get started"
echo ""
