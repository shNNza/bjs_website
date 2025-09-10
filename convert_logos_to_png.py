#!/usr/bin/env python3
"""
Convert all logo files to PNG format for consistent display
"""
import os
from PIL import Image
import cairosvg
from io import BytesIO

# Directory containing the logos
logo_dir = r"C:\Users\Kyle Whitfield\Documents\development\bjs_website\website\static\website\images\logos"

# Files to convert (based on our directory listing)
files_to_convert = [
    ("acer.svg", "acer.png"),
    ("asus.svg", "asus.png"), 
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

def convert_svg_to_png(svg_path, png_path, width=400, height=300):
    """Convert SVG to PNG"""
    try:
        cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=width, output_height=height)
        print(f"✓ Converted {os.path.basename(svg_path)} to PNG")
        return True
    except Exception as e:
        print(f"✗ Error converting {os.path.basename(svg_path)}: {e}")
        return False

def convert_image_to_png(input_path, output_path):
    """Convert other image formats to PNG with white background"""
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
        
        success = False
        
        if original_file.endswith('.svg'):
            success = convert_svg_to_png(input_path, output_path)
        else:
            success = convert_image_to_png(input_path, output_path)
        
        if success:
            converted += 1
        else:
            failed += 1
    
    print(f"\nConversion complete!")
    print(f"✓ Successfully converted: {converted} files")
    print(f"✗ Failed to convert: {failed} files")
    
    if converted > 0:
        print("\nNext step: Update the HTML template to use .png extensions for these files")

if __name__ == "__main__":
    main()