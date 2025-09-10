#!/usr/bin/env python3
"""
Convert all logo files (except SVG) to PNG format for consistent display
"""
import os
from PIL import Image

# Directory containing the logos
logo_dir = r"C:\Users\Kyle Whitfield\Documents\development\bjs_website\website\static\website\images\logos"

# Files to convert (excluding SVG files for now)
files_to_convert = [
    ("atess.webp", "atess.png"),
    ("cisco.webp", "cisco.png"),
    ("Deye.jpg", "deye.png"),
    ("dyness.webp", "dyness.png"),
    ("ghtl.jpeg", "ghtl.png"),
    ("Huawei.jpg", "huawei.png"),
    ("jinko.webp", "jinko.png"),
    ("longi.webp", "longi.png"),
    ("megarevo.webp", "megarevo.png"),
    ("shoto.webp", "shoto.png"),
    ("solis.jpg", "solis.png"),
    ("sunsynk.jpg", "sunsynk.png"),
    ("victron.jpg", "victron.png")
]

def convert_image_to_png(input_path, output_path):
    """Convert image formats to PNG with white background"""
    try:
        # Open the image
        img = Image.open(input_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create a white background
        background = Image.new('RGBA', img.size, (255, 255, 255, 255))
        
        # Paste the image onto white background
        background.paste(img, (0, 0), img)
        
        # Convert to RGB (removes alpha channel)
        final_img = background.convert('RGB')
        
        # Save as PNG
        final_img.save(output_path, 'PNG', quality=95, optimize=True)
        print(f"✓ Converted {os.path.basename(input_path)} to PNG")
        return True
    except Exception as e:
        print(f"✗ Error converting {os.path.basename(input_path)}: {e}")
        return False

def main():
    print("Starting logo conversion to PNG format...")
    print(f"Working directory: {logo_dir}")
    
    if not os.path.exists(logo_dir):
        print(f"Error: Directory {logo_dir} does not exist!")
        return
    
    converted = 0
    failed = 0
    
    for original_file, new_file in files_to_convert:
        input_path = os.path.join(logo_dir, original_file)
        output_path = os.path.join(logo_dir, new_file)
        
        # Skip if input file doesn't exist
        if not os.path.exists(input_path):
            print(f"⚠ Skipping {original_file} - file not found")
            continue
        
        # Skip if output already exists
        if os.path.exists(output_path):
            print(f"⚠ Skipping {new_file} - already exists")
            continue
        
        success = convert_image_to_png(input_path, output_path)
        
        if success:
            converted += 1
        else:
            failed += 1
    
    print(f"\nConversion complete!")
    print(f"✓ Successfully converted: {converted} files")
    print(f"✗ Failed to convert: {failed} files")
    
    print("\nNote: SVG files (acer.svg, asus.svg) kept as-is since they should work fine.")
    
    if converted > 0:
        print("\nNext step: Update the HTML template to use .png extensions for the converted files")

if __name__ == "__main__":
    main()