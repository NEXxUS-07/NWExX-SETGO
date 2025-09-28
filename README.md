# NWExX Stego Linker 🎯

**Create Clickable Media with Hidden Links - Steganography & Web Generation**

A powerful Python CLI tool that generates interactive web pages where images or videos become clickable elements that either redirect to custom URLs or reveal embedded content. Features advanced steganography capabilities to hide URLs invisibly within image data.

## 🚀 Features

- **Interactive Menu System** - User-friendly interface with colorful ASCII art logo
- **Multiple Output Formats** - HTML pages, SVG files, Markdown snippets
- **Steganography Support** - Hide URLs invisibly inside images using LSB (Least Significant Bit) technique
- **Dual Click Modes**:
  - **Redirect Mode**: Opens target URL in new tab
  - **Embed Mode**: Toggles iframe preview of target URL
- **Wide Media Support** - Images (PNG, JPG, JPEG, GIF, WebP, BMP, SVG) and Videos (MP4, WebM, OGG, MOV, MKV)
- **Easy Deployment** - Ready for GitHub Pages hosting

## 🎨 Brand

**NWExX** - Created by Kaushik  
*Professional steganography and web generation tools*

## 📋 Requirements

- Python 3.9+
- Pillow (PIL) - Required for steganography features
  ```bash
  pip install Pillow
  ```

## 🛠️ Installation

No complex installation needed. The script is self-contained:

```bash
git clone <repository-url>
cd stego-linker
# Install Pillow for steganography features
pip install Pillow
```

## 🚀 Usage

### Interactive Mode (Recommended)

Run the script without arguments to access the interactive menu:

```bash
python3 stego_linker.py
```

This will display the NWExX logo and present you with a menu of options:

1. 📄 Generate HTML page (redirect mode)
2. 📄 Generate HTML page (embed mode)  
3. 🖼️ Generate clickable SVG
4. 📝 Generate Markdown snippet
5. 🔐 Generate with steganography (hidden URL)
6. 🌐 Serve generated content
7. ℹ️ Show help and examples
8. ❌ Exit

### Command Line Mode

For automated usage:

```bash
python3 stego_linker.py --media ./path/to/media --url https://your-target-url --mode redirect --out ./Stegno_Templates
```

#### Parameters

- **--media**: Path to your image or video file
- **--url**: Target URL (must start with http:// or https://)
- **--mode**: `redirect` (default) or `embed`
- **--title**: Page title (default: "Clickable Media")
- **--out**: Output directory (default: `./Stegno_Templates`)
- **--format**: `html` (default), `markdown`, or `svg`
- **--stego**: Enable steganography (hides URL in image data)
- **--serve**: Start local server after generation
- **--interactive, -i**: Force interactive mode

## 📁 Output Directory

All generated files are saved to the `Stegno_Templates` directory in your current working directory. This ensures:

- ✅ No root access required
- ✅ Easy file management
- ✅ Direct access to generated content
- ✅ Ready for version control

## 🎯 Examples

### Basic HTML Redirect
```bash
python3 stego_linker.py --media ./assets/photo.jpg --url https://example.com --mode redirect
```

### HTML with Embed Mode
```bash
python3 stego_linker.py --media ./assets/video.mp4 --url https://example.com --mode embed
```

### Clickable SVG
```bash
python3 stego_linker.py --media ./assets/logo.png --url https://example.com --format svg
```

### Steganography (Hidden URL)
```bash
python3 stego_linker.py --media ./assets/photo.jpg --url https://example.com --stego
```
This creates a `*_stego.png` file with the URL invisibly embedded.

### Markdown Snippet
```bash
python3 stego_linker.py --media ./assets/image.jpg --url https://example.com --format markdown
```

## 🌐 Local Preview

```bash
python3 stego_linker.py --serve
# or manually:
python3 -m http.server --directory ./Stegno_Templates 8080
```

Open `http://localhost:8080` in your browser.

## 📤 Deploy to GitHub Pages

1. **Create Repository**: Create a new GitHub repository
2. **Upload Files**: Copy contents of `Stegno_Templates/` to your repo root
3. **Enable Pages**: Go to Settings → Pages → Deploy from branch `main` → `/ (root)`
4. **Access**: Your site will be available at `https://<username>.github.io/<repo>/`

### Quick Deploy Commands
```bash
git init
git add .
git commit -m "Deploy NWExX Stego Linker page"
git branch -M main
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```

## 🔐 Steganography Features

The tool includes advanced steganography capabilities:

- **LSB Embedding**: Hides URLs in the least significant bits of image pixels
- **Invisible Storage**: URLs are completely hidden from visual inspection
- **PNG Output**: Generates optimized PNG files with embedded data
- **Capacity Management**: Automatically checks if image has enough space for the URL

## 🎨 Supported Formats

### Images
- PNG, JPG, JPEG, GIF, WebP, BMP, SVG

### Videos  
- MP4, WebM, OGG, MOV, MKV

## 🔧 Technical Details

- **Privacy-First**: Uses `referrerpolicy="no-referrer"` and `noopener,noreferrer`
- **Responsive Design**: Works on desktop and mobile devices
- **Cross-Platform**: Compatible with Windows, macOS, and Linux
- **No Dependencies**: Core functionality works without external libraries
- **Steganography**: Requires Pillow for LSB embedding features

## ⚠️ Important Notes

- **Steganography**: This is not cryptographic steganography; it's for hiding URLs in image data
- **Iframe Limitations**: Some sites block embedding via X-Frame-Options/CSP headers
- **File Size**: Steganography increases file size slightly due to PNG optimization
- **URL Length**: Very long URLs may not fit in small images

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📄 License

MIT License - Feel free to use this tool for personal or commercial projects.

---

**Created by Kaushik | NWExX Tools** 🎯