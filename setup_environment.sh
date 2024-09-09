#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Please install Python and try again."
    exit 1
fi

# Check if virtual environment exists, create if it doesn't
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt

# Verify installation
echo "Verifying installation..."
pip list

# Run the script
echo "Running ndi_decoder_control.py..."
python ndi_decoder_control.py

# Deactivate virtual environment
deactivate

echo "Setup complete. You can now run 'python ndi_decoder_control.py' in the activated virtual environment."