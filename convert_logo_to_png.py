#!/usr/bin/env python3
"""
Convert logo.jpg to logo.png
"""

import os
from PIL import Image

def convert_logo_to_png():
    """
    Convert the existing logo.jpg to logo.png
    """
    # Define paths
    logo_dir = r"C:\Users\Kyle Whitfield\Documents\development\bjs_website\website\static\website\images\logo"
    jpg_path = os.path.join(logo_dir, "logo.jpg")
    png_path = os.path.join(logo_dir, "logo.png")
    
    # Check if JPG file exists
    if not os.path.exists(jpg_path):
        print(f"JPG file not found: {jpg_path}")
        return
    
    print("Converting logo.jpg to logo.png...")
    print("=" * 40)
    
    try:
        # Open the JPG image
        with Image.open(jpg_path) as img:
            print(f"Original JPG: {img.size} pixels, mode: {img.mode}")
            
            # Convert to RGBA (supports transparency)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
                print("Converted to RGBA mode for transparency support")
            
            # Save as PNG
            img.save(png_path, 'PNG', optimize=True)
            
            # Get file sizes
            jpg_size = os.path.getsize(jpg_path) / 1024  # KB
            png_size = os.path.getsize(png_path) / 1024  # KB
            
            print(f"PNG created: {img.size} pixels")
            print(f"JPG size: {jpg_size:.1f} KB")
            print(f"PNG size: {png_size:.1f} KB")
            print("-" * 40)
            print("✓ Conversion complete!")
            print(f"✓ PNG file saved: {png_path}")
            
    except Exception as e:
        print(f"Error converting logo: {e}")

if __name__ == "__main__":
    convert_logo_to_png()