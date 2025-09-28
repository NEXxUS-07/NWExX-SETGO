#!/bin/bash
# NWExX Stego Linker Installation Script

echo "🎯 Installing NWExX Stego Linker..."
echo "=================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.9 or higher and try again."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.9 or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"

# Install requirements
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Make the script executable
chmod +x stego_linker.py

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Usage:"
echo "  python3 stego_linker.py --interactive"
echo "  python3 stego_linker.py --help"
echo ""
echo "For more information, see README.md"
