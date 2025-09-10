#!/usr/bin/env python3
"""
Make the logo PNG background transparent by removing white pixels
"""

import os
from PIL import Image

def make_logo_transparent():
    """
    Make the logo background transparent by removing white/near-white pixels
    """
    # Define paths
    logo_dir = r"C:\Users\Kyle Whitfield\Documents\development\bjs_website\website\static\website\images\logo"
    png_path = os.path.join(logo_dir, "logo.png")
    transparent_path = os.path.join(logo_dir, "logo_transparent.png")
    
    # Check if PNG file exists
    if not os.path.exists(png_path):
        print(f"PNG file not found: {png_path}")
        return
    
    print("Making logo background transparent...")
    print("=" * 40)
    
    try:
        # Open the PNG image
        with Image.open(png_path) as img:
            print(f"Original PNG: {img.size} pixels, mode: {img.mode}")
            
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Get image data
            data = img.getdata()
            
            # Create new data with transparent background
            new_data = []
            for pixel in data:
                # If pixel is white or very close to white, make it transparent
                r, g, b = pixel[:3]
                if r > 240 and g > 240 and b > 240:  # White or near-white
                    new_data.append((r, g, b, 0))  # Make transparent
                else:
                    new_data.append(pixel)  # Keep original
            
            # Create new image with transparent background
            transparent_img = Image.new('RGBA', img.size)
            transparent_img.putdata(new_data)
            
            # Save the transparent version
            transparent_img.save(transparent_path, 'PNG')
            
            # Replace the original with transparent version
            transparent_img.save(png_path, 'PNG')
            
            print(f"Transparent PNG created: {img.size} pixels")
            print(f"White pixels made transparent")
            print("-" * 40)
            print("Conversion complete!")
            print(f"Transparent logo saved: {png_path}")
            
    except Exception as e:
        print(f"Error making logo transparent: {e}")

if __name__ == "__main__":
    make_logo_transparent()