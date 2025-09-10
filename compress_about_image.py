#!/usr/bin/env python3
"""
Image compression script for about1.jpg
Compresses the about section image to web-optimized size while maintaining quality
"""

import os
from PIL import Image

def compress_about_image():
    """
    Compress about1.jpg for web use
    """
    # Define paths
    about_dir = r"C:\Users\Kyle Whitfield\Documents\development\bjs_website\website\static\website\images\about"
    input_file = "about1.jpg"
    input_path = os.path.join(about_dir, input_file)
    
    # Check if directory exists
    if not os.path.exists(about_dir):
        print(f"About directory not found: {about_dir}")
        return
    
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        return
    
    print("Starting about1.jpg compression...")
    print("=" * 50)
    
    try:
        # Open the image
        with Image.open(input_path) as img:
            original_size_mb = os.path.getsize(input_path) / (1024*1024)
            print(f"Original size: {img.size} ({original_size_mb:.1f} MB)")
            
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # For about section, we want good quality but reasonable size
            # Target size: max 1200px width (suitable for about section)
            max_width = 1200
            max_height = 800
            quality = 85
            
            # Calculate new size maintaining aspect ratio
            width, height = img.size
            aspect_ratio = width / height
            
            if width > max_width or height > max_height:
                if aspect_ratio > max_width / max_height:
                    # Width is the limiting factor
                    new_width = max_width
                    new_height = int(max_width / aspect_ratio)
                else:
                    # Height is the limiting factor
                    new_height = max_height
                    new_width = int(max_height * aspect_ratio)
                
                # Resize image
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                print(f"Resized to: {img.size}")
            
            # Create backup of original
            backup_path = os.path.join(about_dir, "about1_original.jpg")
            if not os.path.exists(backup_path):
                # Make a copy of the original first
                original_img = Image.open(input_path)
                if original_img.mode in ('RGBA', 'P'):
                    original_img = original_img.convert('RGB')
                original_img.save(backup_path, 'JPEG', quality=95)
                print(f"Original backed up as about1_original.jpg")
            
            # Save compressed version
            img.save(input_path, 'JPEG', quality=quality, optimize=True)
            
            compressed_size_mb = os.path.getsize(input_path) / (1024*1024)
            compression_ratio = original_size_mb / compressed_size_mb
            
            print(f"Compressed size: {compressed_size_mb:.1f} MB")
            print(f"Compression ratio: {compression_ratio:.1f}x smaller")
            print(f"Savings: {original_size_mb - compressed_size_mb:.1f} MB")
            print("-" * 50)
            print("Compression complete!")
            
    except Exception as e:
        print(f"Error processing about1.jpg: {e}")

if __name__ == "__main__":
    compress_about_image()