#!/usr/bin/env python3
"""
Example usage of NWExX Stego Linker
This script demonstrates various ways to use the stego_linker module
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import stego_linker
sys.path.insert(0, str(Path(__file__).parent.parent))

from stego_linker import main

def example_basic_redirect():
    """Example: Basic redirect mode"""
    print("🎯 Example 1: Basic Redirect Mode")
    print("=" * 40)
    
    # Simulate command line arguments
    args = [
        "--media", "example_image.jpg",
        "--url", "https://example.com",
        "--mode", "redirect",
        "--title", "My Clickable Image",
        "--out", "./Stegno_Templates"
    ]
    
    print("Command:", " ".join(["python3 stego_linker.py"] + args))
    print("This creates an HTML page that redirects to the URL when clicked.")
    print()

def example_embed_mode():
    """Example: Embed mode"""
    print("🎯 Example 2: Embed Mode")
    print("=" * 40)
    
    args = [
        "--media", "example_video.mp4",
        "--url", "https://example.com",
        "--mode", "embed",
        "--title", "My Embedded Content",
        "--out", "./Stegno_Templates"
    ]
    
    print("Command:", " ".join(["python3 stego_linker.py"] + args))
    print("This creates an HTML page with an iframe that toggles on click.")
    print()

def example_steganography():
    """Example: Steganography mode"""
    print("🎯 Example 3: Steganography Mode")
    print("=" * 40)
    
    args = [
        "--media", "example_image.jpg",
        "--url", "https://example.com",
        "--stego",
        "--title", "Hidden URL Image",
        "--out", "./Stegno_Templates"
    ]
    
    print("Command:", " ".join(["python3 stego_linker.py"] + args))
    print("This creates an image with the URL hidden inside using LSB steganography.")
    print()

def example_svg_format():
    """Example: SVG format"""
    print("🎯 Example 4: SVG Format")
    print("=" * 40)
    
    args = [
        "--media", "example_logo.png",
        "--url", "https://example.com",
        "--format", "svg",
        "--out", "./Stegno_Templates"
    ]
    
    print("Command:", " ".join(["python3 stego_linker.py"] + args))
    print("This creates a standalone clickable SVG file.")
    print()

def example_markdown():
    """Example: Markdown format"""
    print("🎯 Example 5: Markdown Format")
    print("=" * 40)
    
    args = [
        "--media", "example_image.jpg",
        "--url", "https://example.com",
        "--format", "markdown",
        "--out", "./Stegno_Templates"
    ]
    
    print("Command:", " ".join(["python3 stego_linker.py"] + args))
    print("This creates a Markdown snippet for GitHub README files.")
    print()

def main_examples():
    """Run all examples"""
    print("🎯 NWExX Stego Linker - Usage Examples")
    print("=" * 50)
    print()
    
    example_basic_redirect()
    example_embed_mode()
    example_steganography()
    example_svg_format()
    example_markdown()
    
    print("🎉 All examples completed!")
    print()
    print("To run the actual tool:")
    print("  python3 stego_linker.py --interactive")
    print("  python3 stego_linker.py --help")

if __name__ == "__main__":
    main_examples()
