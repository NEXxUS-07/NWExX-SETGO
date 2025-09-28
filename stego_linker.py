#!/usr/bin/env python3
"""
stego_linker.py

Generate a static webpage where an image or video is displayed and, on click,
either redirects to a target URL or reveals an embedded URL preview.

Usage (examples):
  python stego_linker.py --media ./assets/photo.jpg --url https://example.com --mode redirect --out ./Stegno_Templates
  python stego_linker.py --media ./assets/clip.mp4  --url https://example.com --mode embed    --out ./Stegno_Templates

Then host with:
  python -m http.server --directory ./Stegno_Templates 8080

Upload the generated ./Stegno_Templates folder to GitHub (or push and enable GitHub Pages).
"""

import argparse
import os
import shutil
import sys
from pathlib import Path
import base64
from typing import Optional, Tuple
import http.server
import socketserver
from functools import partial
import time

try:
    from PIL import Image  # type: ignore
except ImportError:  # pragma: no cover
    Image = None  # Pillow is optional unless --stego is used


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg"}
VIDEO_EXTS = {".mp4", ".webm", ".ogg", ".mov", ".mkv"}

# ANSI color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_logo():
    """Display the NWExX Tools logo with skull background"""
    logo = f"""
{Colors.BLUE}{Colors.BOLD}
'     _______  __      _____________       ____  ___     ___________________   ________  .____       _________             
'     \      \/  \    /  \_   _____/__  ___\   \/  /     \__    ___/\_____  \  \_____  \ |    |     /   _____/             
'     /   |   \   \/\/   /|    __)_\  \/  / \     /        |    |    /   |   \  /   |   \|    |     \_____  \              
'    /    |    \        / |        \>    <  /     \        |    |   /    |    \/    |    \    |___  /        \             
'    \____|__  /\__/\  / /_______  /__/\_ \/___/\  \       |____|   \_______  /\_______  /_______ \/_______  /  /\  /\  /\ 
'            \/      \/          \/      \/      \_/                        \/         \/        \/        \/   \/  \/  \/ 
                                                                                             
                                                                                             by Kaushik
                                                                                             github link:https://github.com/NEXxUS-07



                                                                                             
{Colors.END}
"""
    print(logo)
    time.sleep(1)

def print_menu():
    """Display the main menu options"""
    print(f"\n{Colors.YELLOW}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.YELLOW}{Colors.BOLD}║                    🎯 MAIN MENU OPTIONS                      ║{Colors.END}")
    print(f"{Colors.YELLOW}{Colors.BOLD}╚══════════════════════════════════════════════════════════════╝{Colors.END}")
    print(f"\n{Colors.GREEN}1.{Colors.END} 📄 Generate HTML page (redirect mode)")
    print(f"{Colors.GREEN}2.{Colors.END} 📄 Generate HTML page (embed mode)")
    print(f"{Colors.GREEN}3.{Colors.END} 🖼️  Generate clickable SVG")
    print(f"{Colors.GREEN}4.{Colors.END} 📝 Generate Markdown snippet")
    print(f"{Colors.GREEN}5.{Colors.END} 🔐 Generate with steganography (hidden URL)")
    print(f"{Colors.GREEN}6.{Colors.END} 🌐 Serve generated content")
    print(f"{Colors.GREEN}7.{Colors.END} ℹ️  Show help and examples")
    print(f"{Colors.RED}8.{Colors.END} ❌ Exit")
    print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")

def get_user_choice():
    """Get user choice from menu"""
    while True:
        try:
            choice = input(f"\n{Colors.BLUE}Enter your choice (1-8): {Colors.END}").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                return int(choice)
            else:
                print(f"{Colors.RED}❌ Invalid choice! Please enter a number between 1-8.{Colors.END}")
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}👋 Goodbye!{Colors.END}")
            sys.exit(0)
        except EOFError:
            print(f"\n{Colors.YELLOW}👋 Goodbye!{Colors.END}")
            sys.exit(0)

def get_media_path():
    """Get media file path from user"""
    while True:
        media_path = input(f"{Colors.BLUE}📁 Enter path to media file: {Colors.END}").strip()
        if not media_path:
            print(f"{Colors.RED}❌ Please enter a valid file path.{Colors.END}")
            continue
        
        path = Path(media_path).expanduser().resolve()
        if not path.exists() or not path.is_file():
            print(f"{Colors.RED}❌ File not found: {path}{Colors.END}")
            continue
        
        ext = path.suffix.lower()
        if ext not in IMAGE_EXTS and ext not in VIDEO_EXTS:
            print(f"{Colors.RED}❌ Unsupported file type: {ext}{Colors.END}")
            print(f"{Colors.YELLOW}Supported formats: {sorted(IMAGE_EXTS | VIDEO_EXTS)}{Colors.END}")
            continue
        
        return path

def get_target_url():
    """Get target URL from user"""
    while True:
        url = input(f"{Colors.BLUE}🔗 Enter target URL: {Colors.END}").strip()
        if not url:
            print(f"{Colors.RED}❌ Please enter a valid URL.{Colors.END}")
            continue
        
        if not (url.startswith("http://") or url.startswith("https://")):
            print(f"{Colors.RED}❌ URL must start with http:// or https://{Colors.END}")
            continue
        
        return url

def get_output_directory():
    """Get output directory from user"""
    out_dir = input(f"{Colors.BLUE}📂 Enter output directory (default: ./Stegno_Templates): {Colors.END}").strip()
    if not out_dir:
        out_dir = "./Stegno_Templates"
    
    # Ensure the path is relative to current working directory
    if not out_dir.startswith('/'):
        out_dir = os.path.join(os.getcwd(), out_dir)
    
    return Path(out_dir).resolve()

def get_title():
    """Get page title from user"""
    title = input(f"{Colors.BLUE}📝 Enter page title (default: Clickable Media): {Colors.END}").strip()
    if not title:
        title = "Clickable Media"
    return title

def show_help():
    """Display help and examples"""
    help_text = f"""
{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗{Colors.END}
{Colors.CYAN}{Colors.BOLD}║                        📚 HELP & EXAMPLES                  ║{Colors.END}
{Colors.CYAN}{Colors.BOLD}╚══════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.GREEN}🎯 What is Stego Linker?{Colors.END}
Stego Linker creates clickable media (images/videos) that redirect to URLs or embed content.
It can also hide URLs invisibly inside images using steganography.

{Colors.GREEN}📋 Supported Formats:{Colors.END}
• Images: PNG, JPG, JPEG, GIF, WebP, BMP, SVG
• Videos: MP4, WebM, OGG, MOV, MKV

{Colors.GREEN}🔧 Modes:{Colors.END}
• {Colors.BLUE}Redirect:{Colors.END} Clicking opens URL in new tab
• {Colors.BLUE}Embed:{Colors.END} Clicking shows/hides embedded iframe
• {Colors.BLUE}Steganography:{Colors.END} Hides URL invisibly in image data

{Colors.GREEN}📝 Examples:{Colors.END}
• Generate HTML redirect: python stego_linker.py --media photo.jpg --url https://example.com
• Generate with embed: python stego_linker.py --media video.mp4 --url https://example.com --mode embed
• Generate SVG: python stego_linker.py --media logo.png --url https://example.com --format svg
• Generate with stego: python stego_linker.py --media photo.jpg --url https://example.com --stego

{Colors.GREEN}🌐 Deployment:{Colors.END}
• Upload the generated ./Stegno_Templates folder to GitHub
• Enable GitHub Pages for automatic hosting
• Or serve locally with: python -m http.server --directory ./Stegno_Templates 8080
"""
    print(help_text)
    input(f"\n{Colors.BLUE}Press Enter to continue...{Colors.END}")

def interactive_mode():
    """Run the interactive menu system"""
    print_logo()
    
    while True:
        print_menu()
        choice = get_user_choice()
        
        if choice == 8:  # Exit
            print(f"\n{Colors.GREEN}👋 Thank you for using Stego Linker! Goodbye!{Colors.END}")
            break
        
        try:
            if choice == 1:  # HTML redirect
                media_path = get_media_path()
                url = get_target_url()
                out_dir = get_output_directory()
                title = get_title()
                
                print(f"\n{Colors.YELLOW}🔄 Generating HTML redirect page...{Colors.END}")
                result = run_generation(media_path, url, "redirect", out_dir, title, "html", False, False)
                if result == 0:
                    print(f"{Colors.GREEN}✅ HTML redirect page generated successfully!{Colors.END}")
                
            elif choice == 2:  # HTML embed
                media_path = get_media_path()
                url = get_target_url()
                out_dir = get_output_directory()
                title = get_title()
                
                print(f"\n{Colors.YELLOW}🔄 Generating HTML embed page...{Colors.END}")
                result = run_generation(media_path, url, "embed", out_dir, title, "html", False, False)
                if result == 0:
                    print(f"{Colors.GREEN}✅ HTML embed page generated successfully!{Colors.END}")
                
            elif choice == 3:  # SVG
                media_path = get_media_path()
                url = get_target_url()
                out_dir = get_output_directory()
                
                print(f"\n{Colors.YELLOW}🔄 Generating clickable SVG...{Colors.END}")
                result = run_generation(media_path, url, "redirect", out_dir, "Clickable Media", "svg", False, False)
                if result == 0:
                    print(f"{Colors.GREEN}✅ Clickable SVG generated successfully!{Colors.END}")
                
            elif choice == 4:  # Markdown
                media_path = get_media_path()
                url = get_target_url()
                out_dir = get_output_directory()
                
                print(f"\n{Colors.YELLOW}🔄 Generating Markdown snippet...{Colors.END}")
                result = run_generation(media_path, url, "redirect", out_dir, "Clickable Media", "markdown", False, False)
                if result == 0:
                    print(f"{Colors.GREEN}✅ Markdown snippet generated successfully!{Colors.END}")
                
            elif choice == 5:  # Steganography
                media_path = get_media_path()
                url = get_target_url()
                out_dir = get_output_directory()
                title = get_title()
                
                print(f"\n{Colors.YELLOW}🔄 Generating with steganography...{Colors.END}")
                result = run_generation(media_path, url, "redirect", out_dir, title, "html", True, False)
                if result == 0:
                    print(f"{Colors.GREEN}✅ Steganography page generated successfully!{Colors.END}")
                
            elif choice == 6:  # Serve
                out_dir = get_output_directory()
                if not out_dir.exists():
                    print(f"{Colors.RED}❌ Output directory does not exist: {out_dir}{Colors.END}")
                    continue
                
                host = input(f"{Colors.BLUE}🌐 Enter host (default: 0.0.0.0): {Colors.END}").strip() or "0.0.0.0"
                try:
                    port = int(input(f"{Colors.BLUE}🔌 Enter port (default: 8080): {Colors.END}").strip() or "8080")
                except ValueError:
                    port = 8080
                
                print(f"\n{Colors.YELLOW}🔄 Starting server...{Colors.END}")
                serve_directory(out_dir, host, port)
                
            elif choice == 7:  # Help
                show_help()
                continue
        
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}👋 Operation cancelled. Returning to menu...{Colors.END}")
            continue
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.END}")
            continue
        
        # Ask if user wants to continue
        continue_choice = input(f"\n{Colors.BLUE}🔄 Would you like to perform another operation? (y/n): {Colors.END}").strip().lower()
        if continue_choice not in ['y', 'yes']:
            print(f"\n{Colors.GREEN}👋 Thank you for using Stego Linker! Goodbye!{Colors.END}")
            break

def run_generation(media_path: Path, url: str, mode: str, out_dir: Path, title: str, format_type: str, stego: bool, serve: bool) -> int:
    """Run the generation process with given parameters"""
    # This is a simplified version of the main function logic
    error = validate_inputs(media_path, url, mode)
    if error:
        print(f"{Colors.RED}❌ Error: {error}{Colors.END}")
        return 2

    # Prepare output
    if not out_dir.exists():
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"{Colors.GREEN}📁 Created directory: {out_dir}{Colors.END}")
    else:
        print(f"{Colors.BLUE}📁 Using existing directory: {out_dir}{Colors.END}")

    # Copy media to output directory
    media_filename = copy_media(media_path, out_dir)
    media_kind = "image" if media_path.suffix.lower() in IMAGE_EXTS else "video"

    # Optionally embed the URL invisibly into a PNG
    stego_filename: Optional[str] = None
    if stego and media_kind == "image":
        try:
            stego_filename = derive_stego_name(media_filename)
            embed_lsb_message_into_image(out_dir / media_filename, url, out_dir / stego_filename)
            print(f"{Colors.GREEN}🔐 Embedded hidden URL into: {out_dir / stego_filename}{Colors.END}")
        except Exception as exc:
            print(f"{Colors.RED}❌ Error embedding stego message: {exc}{Colors.END}")
            return 2

    if format_type == "markdown":
        md_image = stego_filename or media_filename
        snippet = f"[![clickable media]({md_image})]({url})\n"
        write_file(out_dir / "README_snippet.md", snippet)
        print(f"{Colors.GREEN}📝 Markdown snippet created: {out_dir / 'README_snippet.md'}{Colors.END}")
        return 0

    if format_type == "svg":
        svg_source = out_dir / (stego_filename or media_filename)
        svg_content = generate_clickable_svg(svg_source, url)
        svg_name = f"{Path(svg_source).stem}.svg"
        svg_path = out_dir / svg_name
        write_file(svg_path, svg_content)
        print(f"{Colors.GREEN}🖼️ Clickable SVG created: {svg_path}{Colors.END}")
        return 0

    # Default: HTML output
    html = generate_html(
        title=title,
        media_filename=media_filename,
        media_kind=media_kind,
        target_url=url,
        mode=mode,
    )
    write_file(out_dir / "index.html", html)
    write_file(out_dir / ".nojekyll", "")
    print(f"{Colors.GREEN}📄 HTML page created: {out_dir / 'index.html'}{Colors.END}")
    
    return 0


def validate_inputs(media_path: Path, url: str, mode: str) -> str:
    if not media_path.exists() or not media_path.is_file():
        return f"Media file not found: {media_path}"
    if not (url.startswith("http://") or url.startswith("https://")):
        return "--url must start with http:// or https://"
    if mode not in {"redirect", "embed"}:
        return "--mode must be either 'redirect' or 'embed'"
    ext = media_path.suffix.lower()
    if ext not in IMAGE_EXTS and ext not in VIDEO_EXTS:
        return (
            f"Unsupported media extension '{ext}'. Supported images: {sorted(IMAGE_EXTS)}; "
            f"videos: {sorted(VIDEO_EXTS)}"
        )
    return ""


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def copy_media(src: Path, dest_dir: Path) -> str:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / src.name
    shutil.copy2(src, dest_path)
    return dest_path.name


def guess_image_mime(ext: str) -> str:
    ext = ext.lower()
    if ext == ".png":
        return "image/png"
    if ext in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if ext == ".gif":
        return "image/gif"
    if ext == ".webp":
        return "image/webp"
    if ext == ".bmp":
        return "image/bmp"
    if ext == ".svg":
        return "image/svg+xml"
    # Fallback
    return "application/octet-stream"


def generate_clickable_svg(image_path: Path, target_url: str) -> str:
    # Embed the raster/vector image as a data URI and wrap in an <a> link.
    # Add a transparent rect so the entire SVG area is clickable.
    data = image_path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    mime = guess_image_mime(image_path.suffix)
    data_uri = f"data:{mime};base64,{b64}"
    escaped_url = html_escape(target_url)

    # Try to use real intrinsic size if Pillow is available; otherwise fallback to 100x100 viewBox
    vb_w = 100
    vb_h = 100
    if Image is not None:
        try:
            with Image.open(image_path) as im:
                vb_w, vb_h = im.size
        except Exception:
            pass

    onclick_js = "try{window.top.location.href='" + escaped_url + "'}catch(e){window.location.href='" + escaped_url + "'}"
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100%" height="100%" viewBox="0 0 {vb_w} {vb_h}" preserveAspectRatio="xMidYMid meet" style="cursor:pointer" onclick="{onclick_js}" role="link" aria-label="Open link">
      <title>Open link</title>
      <a xlink:href="{escaped_url}" href="{escaped_url}" target="_top">
        <rect x="0" y="0" width="100%" height="100%" fill="transparent"/>
        <image x="0" y="0" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" xlink:href="{data_uri}" href="{data_uri}"/>
      </a>
    </svg>
    """
    return svg


def ensure_pillow_installed() -> None:
    if Image is None:
        print(
            "Error: Pillow is required for steganography. Install with: pip install Pillow",
            file=sys.stderr,
        )
        raise SystemExit(2)


def embed_lsb_message_into_image(source_image_path: Path, message: str, output_image_path: Path) -> None:
    """
    Embed the given message into the LSBs of the image's RGB channels.
    Output is a PNG visually indistinguishable to the naked eye.
    Format: [32-bit message length in bytes][message bytes]
    """
    ensure_pillow_installed()

    img = Image.open(source_image_path).convert("RGB")
    width, height = img.size
    pixels = list(img.getdata())  # list of (r,g,b)

    # Prepare bitstream to embed
    message_bytes = message.encode("utf-8")
    length = len(message_bytes)
    header = length.to_bytes(4, byteorder="big")
    data = header + message_bytes
    bits = []
    for byte in data:
        for bit_idx in range(7, -1, -1):
            bits.append((byte >> bit_idx) & 1)

    capacity_bits = width * height * 3
    if len(bits) > capacity_bits:
        raise ValueError(
            f"Message too large to embed. Available bits: {capacity_bits}, needed: {len(bits)}"
        )

    # Embed bits across pixels' RGB LSBs
    bit_i = 0
    new_pixels = []
    for (r, g, b) in pixels:
        if bit_i < len(bits):
            r = (r & 0xFE) | bits[bit_i]
            bit_i += 1
        if bit_i < len(bits):
            g = (g & 0xFE) | bits[bit_i]
            bit_i += 1
        if bit_i < len(bits):
            b = (b & 0xFE) | bits[bit_i]
            bit_i += 1
        new_pixels.append((r, g, b))

    stego = Image.new("RGB", (width, height))
    stego.putdata(new_pixels)
    output_image_path.parent.mkdir(parents=True, exist_ok=True)
    stego.save(output_image_path, format="PNG", optimize=True)


def derive_stego_name(original_filename: str) -> str:
    stem = Path(original_filename).stem
    return f"{stem}_stego.png"


def generate_html(title: str, media_filename: str, media_kind: str, target_url: str, mode: str) -> str:
    # Minimal page that shows ONLY the clickable media. No headers, no footer.
    # mode == redirect: clicking media opens target_url in new tab
    # mode == embed: clicking media toggles an iframe showing target_url (hidden until clicked)
    escaped_title = html_escape(title)
    escaped_target = html_escape(target_url)
    media_tag = ""
    if media_kind == "image":
        media_tag = f'<img id="media" src="{media_filename}" alt="media" />'
    else:
        # Autoplay is off. Controls shown; click behavior handled by JS.
        media_tag = (
            f'<video id="media" src="{media_filename}" controls preload="metadata"></video>'
        )

    embed_block = (
        """
        <div id="embedContainer" class="hidden">
          <iframe id="embedFrame" src="" loading="lazy" referrerpolicy="no-referrer"></iframe>
        </div>
        """
        if mode == "embed"
        else ""
    )

    script = (
        f"""
        <script>
          (function() {{
            const mode = {mode!r};
            const target = {escaped_target!r};
            const media = document.getElementById('media');
            const embedContainer = document.getElementById('embedContainer');
            const embedFrame = document.getElementById('embedFrame');

            function openInNewTab(url) {{
              window.open(url, '_blank', 'noopener,noreferrer');
            }}

            media.addEventListener('click', function() {{
              if (mode === 'redirect') {{
                openInNewTab(target);
                return;
              }}
              if (mode === 'embed') {{
                if (embedContainer.classList.contains('hidden')) {{
                  embedFrame.src = target;
                  embedContainer.classList.remove('hidden');
                  embedContainer.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }} else {{
                  embedFrame.src = '';
                  embedContainer.classList.add('hidden');
                }}
              }}
            }});
          }})();
        </script>
        """
    )

    styles = """
      :root { color-scheme: light dark; }
      * { box-sizing: border-box; }
      html, body { height: 100%; }
      body {
        margin: 0;
        display: grid;
        place-items: center;
        background: #000;
      }
      #media {
        max-width: 100vw;
        max-height: 100dvh;
        width: auto;
        height: auto;
        cursor: pointer;
        display: block;
      }
      #embedContainer { width: 100%; height: 100%; }
      #embedContainer.hidden { display: none; }
      #embedFrame { width: 100%; height: 100%; border: 0; }
    """

    html = f"""
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <meta name="referrer" content="no-referrer" />
      <title>{escaped_title}</title>
      <style>{styles}</style>
    </head>
    <body>
      {media_tag}
      {embed_block}
      {script}
    </body>
    </html>
    """
    return html


def html_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Generate clickable media output redirecting to or embedding a target URL.")
    parser.add_argument("--media", help="Path to image or video file")
    parser.add_argument("--url", help="Target URL to redirect to or embed")
    parser.add_argument("--mode", choices=["redirect", "embed"], default="redirect", help="Click behavior: redirect (default) or embed")
    parser.add_argument("--title", default="Clickable Media", help="Page title")
    parser.add_argument("--out", default="./Stegno_Templates", help="Output directory for generated files")
    parser.add_argument("--format", choices=["html", "markdown", "svg"], default="html", help="Output format: html (index.html), markdown (README_snippet.md), svg (single clickable image)")
    parser.add_argument("--stego", action="store_true", help="Embed the URL into the image using LSB steganography (outputs *_stego.png)")
    parser.add_argument("--serve", action="store_true", help="After generating, serve the output directory over HTTP")
    parser.add_argument("--host", default="0.0.0.0", help="Host/interface to bind when serving (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8080, help="Port to serve on when --serve is used (default: 8080)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode with menu")
    args = parser.parse_args(argv)
    
    # If no arguments provided or interactive mode requested, run interactive mode
    if not any([args.media, args.url]) or args.interactive:
        interactive_mode()
        return 0

    # Validate required arguments for command-line mode
    if not args.media or not args.url:
        print(f"{Colors.RED}❌ Error: --media and --url are required for command-line mode{Colors.END}")
        print(f"{Colors.YELLOW}💡 Use --interactive or -i for menu mode{Colors.END}")
        return 2

    # Show logo for command-line mode too
    print_logo()
    
    media_path = Path(args.media).expanduser().resolve()
    
    # Ensure output directory is relative to current working directory
    if not args.out.startswith('/'):
        out_dir = Path(os.path.join(os.getcwd(), args.out)).resolve()
    else:
        out_dir = Path(args.out).expanduser().resolve()
    error = validate_inputs(media_path, args.url, args.mode)
    if error:
        print(f"{Colors.RED}❌ Error: {error}{Colors.END}")
        return 2

    # Prepare output
    if not out_dir.exists():
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"{Colors.GREEN}📁 Created directory: {out_dir}{Colors.END}")
    else:
        print(f"{Colors.BLUE}📁 Using existing directory: {out_dir}{Colors.END}")

    # Copy media to output directory
    media_filename = copy_media(media_path, out_dir)
    media_kind = "image" if media_path.suffix.lower() in IMAGE_EXTS else "video"

    # Optionally embed the URL invisibly into a PNG
    stego_filename: Optional[str] = None
    if args.stego and media_kind == "image":
        try:
            stego_filename = derive_stego_name(media_filename)
            embed_lsb_message_into_image(out_dir / media_filename, args.url, out_dir / stego_filename)
            print(f"{Colors.GREEN}🔐 Embedded hidden URL into: {out_dir / stego_filename}{Colors.END}")
        except Exception as exc:  # pragma: no cover
            print(f"{Colors.RED}❌ Error embedding stego message: {exc}{Colors.END}")
            return 2

    if args.format == "markdown":
        # Produce a Markdown snippet that makes the image clickable to the URL.
        md_image = stego_filename or media_filename
        snippet = f"[![clickable media]({md_image})]({args.url})\n"
        write_file(out_dir / "README_snippet.md", snippet)
        print(f"\n{Colors.GREEN}✅ Done. Markdown snippet created:{Colors.END}")
        print(f"  {out_dir / 'README_snippet.md'}")
        print(f"\n{Colors.YELLOW}💡 Use this in your README.md on GitHub to make the image clickable.{Colors.END}")
        if args.serve:
            return serve_directory(out_dir, args.host, args.port)
        return 0

    if args.format == "svg":
        # Create a standalone SVG that, when clicked, opens the URL
        svg_source = out_dir / (stego_filename or media_filename)
        svg_content = generate_clickable_svg(svg_source, args.url)
        svg_name = f"{Path(svg_source).stem}.svg"
        svg_path = out_dir / svg_name
        write_file(svg_path, svg_content)
        print(f"\n{Colors.GREEN}✅ Done. Clickable SVG image created:{Colors.END}")
        print(f"  {svg_path}")
        if stego_filename:
            # Print explicit summary lines for user convenience
            print(f"\n{Colors.CYAN}📋 Summary:{Colors.END}")
            print(f"Hidden-image: {out_dir / stego_filename} (URL embedded, invisible)")
            print(f"Clickable wrapper: {svg_path} (click opens the URL instantly)")
        else:
            print(f"\n{Colors.YELLOW}💡 Tip: Use --stego to also embed the URL invisibly into a PNG next to the SVG.{Colors.END}")
        if args.serve:
            return serve_directory(out_dir, args.host, args.port)
        return 0

    # Default: HTML output
    html = generate_html(
        title=args.title,
        media_filename=media_filename,
        media_kind=media_kind,
        target_url=args.url,
        mode=args.mode,
    )
    write_file(out_dir / "index.html", html)

    # Write a .nojekyll to make GitHub Pages serve files as-is
    write_file(out_dir / ".nojekyll", "")

    print(f"\n{Colors.GREEN}✅ Done. Static page created:{Colors.END}")
    print(f"  {out_dir / 'index.html'}")
    if args.serve:
        return serve_directory(out_dir, args.host, args.port)
    else:
        print(f"\n{Colors.BLUE}🌐 Preview locally:{Colors.END}")
        print(f"  python -m http.server --directory {out_dir} 8080")
        print(f"\n{Colors.YELLOW}📤 Upload the contents of the Stegno_Templates directory to GitHub or push and enable GitHub Pages.{Colors.END}")
        return 0


def serve_directory(directory: Path, host: str, port: int) -> int:
    handler_cls = partial(http.server.SimpleHTTPRequestHandler, directory=str(directory))
    with socketserver.TCPServer((host, port), handler_cls) as httpd:
        print(f"\n{Colors.GREEN}🌐 Serving {directory} on http://{host}:{port}{Colors.END}")
        print(f"{Colors.YELLOW}Press Ctrl+C to stop{Colors.END}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}🛑 Server stopped.{Colors.END}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


