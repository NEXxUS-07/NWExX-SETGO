# 🚀 Quick Start Guide

## Installation

### Linux/macOS
```bash
chmod +x install.sh
./install.sh
```

### Windows
```cmd
install.bat
```

### Manual Installation
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode (Recommended)
```bash
python3 stego_linker.py
```

### Command Line Mode
```bash
python3 stego_linker.py --media image.jpg --url https://example.com --mode redirect
```

## Examples

### Create HTML Redirect Page
```bash
python3 stego_linker.py --media photo.jpg --url https://example.com --mode redirect
```

### Create with Steganography
```bash
python3 stego_linker.py --media photo.jpg --url https://example.com --stego
```

### Generate Clickable SVG
```bash
python3 stego_linker.py --media logo.png --url https://example.com --format svg
```

## Output

All files are saved to the `Stegno_Templates/` directory in your current working directory.

## Need Help?

- Run `python3 stego_linker.py --help` for command line options
- Use interactive mode for guided setup
- Check README.md for detailed documentation

---

**NWExX Tools** - Created by Kaushik
