# Check if Python is installed
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. Please install Python and try again."
    exit 1
}

# Check if virtual environment exists, create if it doesn't
if (!(Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
.\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

# Install required packages
Write-Host "Installing required packages..."
pip install -r requirements.txt

# Verify installation
Write-Host "Verifying installation..."
pip list

# Create executable
Write-Host "Creating executable..."
pyinstaller --onefile --windowed ndi_decoder_control.py

# Deactivate virtual environment
deactivate

Write-Host "Setup complete. The executable is located in the 'dist' folder."