#!/usr/bin/env python3
"""
Fix contact video for web compatibility
Create a better web-compatible version using different codec
"""

import cv2
import os

def fix_contact_video():
    video_dir = "website/static/website/videos/"
    input_file = os.path.join(video_dir, "contact-background.mp4")
    backup_file = os.path.join(video_dir, "contact-background-backup.mp4")
    output_file = os.path.join(video_dir, "contact-background-fixed.mp4")
    
    if not os.path.exists(input_file):
        print("ERROR: Contact video not found")
        return False
    
    print("Creating web-compatible contact video...")
    
    try:
        # Backup current file
        os.rename(input_file, backup_file)
        
        # Open the backup video
        cap = cv2.VideoCapture(backup_file)
        
        if not cap.isOpened():
            print("ERROR: Could not open video file")
            os.rename(backup_file, input_file)  # Restore
            return False
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"Processing video: {width}x{height}, {fps} fps, {total_frames} frames")
        
        # Use MP4V codec which is more web-compatible
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
        
        if not out.isOpened():
            print("ERROR: Could not create output video")
            os.rename(backup_file, input_file)  # Restore
            return False
        
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            out.write(frame)
            frame_count += 1
            
            if frame_count % 50 == 0:
                progress = (frame_count / total_frames) * 100
                print(f"Progress: {progress:.1f}%")
        
        cap.release()
        out.release()
        
        # Replace with fixed version
        if os.path.exists(output_file):
            os.rename(output_file, input_file)
            print("Fixed video created successfully!")
            
            # Check sizes
            original_size = os.path.getsize(backup_file) / (1024 * 1024)
            fixed_size = os.path.getsize(input_file) / (1024 * 1024)
            print(f"Original: {original_size:.1f} MB")
            print(f"Fixed: {fixed_size:.1f} MB")
            
            return True
        else:
            print("ERROR: Fixed video was not created")
            os.rename(backup_file, input_file)  # Restore
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        # Try to restore original
        if os.path.exists(backup_file):
            os.rename(backup_file, input_file)
        return False

if __name__ == "__main__":
    print("Contact Video Web Compatibility Fix")
    print("=" * 40)
    
    success = fix_contact_video()
    
    if success:
        print("Contact video is now web-compatible!")
    else:
        print("Failed to fix contact video.")