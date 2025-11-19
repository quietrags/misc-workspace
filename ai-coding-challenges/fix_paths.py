#!/usr/bin/env python3
"""Fix CSS paths in generated HTML files"""
import os
from pathlib import Path

base_dir = Path('.')

# Files in root directory should use "./styles.css"
root_files = [
    'index.html',
    'quick-start.html',
    'problem-statement.html',
    'ai-modes-guide.html'
]

for filename in root_files:
    filepath = base_dir / filename
    if filepath.exists():
        content = filepath.read_text()
        # Fix the stylesheet path
        content = content.replace('href="../styles.css"', 'href="./styles.css"')
        content = content.replace('href="../index.html"', 'href="./index.html"')
        content = content.replace('href="../quick-start.html"', 'href="./quick-start.html"')
        content = content.replace('href="../ai-modes-guide.html"', 'href="./ai-modes-guide.html"')
        filepath.write_text(content)
        print(f"✅ Fixed paths in {filename}")

print("🎉 Path fixing complete!")
