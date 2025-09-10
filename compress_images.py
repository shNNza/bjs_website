#!/usr/bin/env python3
"""
Image compression script for banner images
Compresses images to web-optimized sizes while maintaining quality
"""

import os
from PIL import Image

def compress_image(input_path, output_path, max_width=1920, max_height=1080, quality=85):
    """
    Compress and resize image for web use
    
    Args:
        input_path (str): Path to original image
        output_path (str): Path to save compressed image
        max_width (int): Maximum width in pixels
        max_height (int): Maximum height in pixels
        quality (int): JPEG quality (1-100, higher is better quality)
    """
    try:
        # Open the image
        with Image.open(input_path) as img:
            print(f"Original size: {img.size} ({os.path.getsize(input_path) / (1024*1024):.1f} MB)")
            
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
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
            
            # Save with compression
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            
            compressed_size = os.path.getsize(output_path) / (1024*1024)
            print(f"Compressed size: {compressed_size:.1f} MB")
            print(f"Compression ratio: {(os.path.getsize(input_path) / os.path.getsize(output_path)):.1f}x smaller")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def main():
    # Define paths
    hero_dir = r"C:\Users\Kyle Whitfield\Documents\development\bjs_website\website\static\website\images\hero"
    
    # Check if directory exists
    if not os.path.exists(hero_dir):
        print(f"Hero directory not found: {hero_dir}")
        return
    
    # List of banner images to compress
    banner_files = ['banner1.jpg', 'banner2.jpg', 'banner3.jpg', 'banner4.jpg']
    
    print("Starting image compression...")
    print("=" * 50)
    
    for banner in banner_files:
        input_path = os.path.join(hero_dir, banner)
        
        if os.path.exists(input_path):
            print(f"Processing {banner}...")
            
            # Create backup of original (if not already exists)
            backup_path = os.path.join(hero_dir, f"{banner.replace('.jpg', '_original.jpg')}")
            if not os.path.exists(backup_path):
                os.rename(input_path, backup_path)
                print(f"Original backed up as {banner.replace('.jpg', '_original.jpg')}")
                input_path = backup_path
            
            # Compress the image
            output_path = os.path.join(hero_dir, banner)
            compress_image(input_path, output_path)
            
        else:
            print(f"File not found: {banner}")
    
    print("Compression complete!")
    print("\nTotal sizes:")
    total_original = 0
    total_compressed = 0
    
    for banner in banner_files:
        original_path = os.path.join(hero_dir, f"{banner.replace('.jpg', '_original.jpg')}")
        compressed_path = os.path.join(hero_dir, banner)
        
        if os.path.exists(original_path):
            orig_size = os.path.getsize(original_path) / (1024*1024)
            total_original += orig_size
            
        if os.path.exists(compressed_path):
            comp_size = os.path.getsize(compressed_path) / (1024*1024)
            total_compressed += comp_size
    
    if total_original > 0:
        print(f"Total original size: {total_original:.1f} MB")
        print(f"Total compressed size: {total_compressed:.1f} MB")
        print(f"Total savings: {total_original - total_compressed:.1f} MB ({(total_original/total_compressed):.1f}x smaller)")

if __name__ == "__main__":
    main()