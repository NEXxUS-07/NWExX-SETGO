#!/usr/bin/env python3
"""
Setup script for NWExX Stego Linker
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nwexx-stego-linker",
    version="1.0.0",
    author="Kaushik",
    author_email="kaushik@nwexx.tools",
    description="Create Clickable Media with Hidden Links - Steganography & Web Generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NEXxUS-07/NWExX-Stego-Linker",
    py_modules=["stego_linker"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Security :: Cryptography",
    ],
    python_requires=">=3.9",
    install_requires=[
        "Pillow>=9.0.0",
    ],
    entry_points={
        "console_scripts": [
            "stego-linker=stego_linker:main",
        ],
    },
    keywords="steganography, web, media, clickable, links, security, tools",
    project_urls={
        "Bug Reports": "https://github.com/NEXxUS-07/NWExX-Stego-Linker/issues",
        "Source": "https://github.com/NEXxUS-07/NWExX-Stego-Linker",
        "Documentation": "https://github.com/NEXxUS-07/NWExX-Stego-Linker#readme",
    },
)
