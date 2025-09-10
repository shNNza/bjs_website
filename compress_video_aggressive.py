#!/usr/bin/env python3
"""
Aggressive video compression script using OpenCV
More aggressive compression settings for web optimization
"""

import cv2
import os
import sys

def compress_video():
    video_dir = "website/static/website/videos/"
    input_file = os.path.join(video_dir, "news-background.mp4")
    output_file = os.path.join(video_dir, "news-background-web.mp4")
    
    if not os.path.exists(input_file):
        print(f"ERROR: Video file not found: {input_file}")
        return False
    
    print(f"Compressing video with aggressive settings: {input_file}")
    print("This may take a few minutes...")
    
    try:
        # Open the input video
        cap = cv2.VideoCapture(input_file)
        
        if not cap.isOpened():
            print("ERROR: Could not open video file")
            return False
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps
        
        print(f"Original video info:")
        print(f"  Resolution: {width}x{height}")
        print(f"  FPS: {fps:.2f}")
        print(f"  Duration: {duration:.2f} seconds")
        
        # More aggressive settings for web background
        target_fps = 15  # Lower fps for smaller file
        target_width = min(1280, width)  # Reduce to 720p width for web
        target_height = int(target_width * height / width)
        
        # Shorter duration for background loops
        max_duration = min(15, duration)  # Max 15 seconds
        max_frames = int(max_duration * target_fps)
        
        print(f"Target video info:")
        print(f"  Resolution: {target_width}x{target_height}")
        print(f"  FPS: {target_fps}")
        print(f"  Duration: {max_duration:.2f} seconds")
        
        # Use H.264 with more aggressive compression
        # FOURCC for better compression
        fourcc = cv2.VideoWriter_fourcc(*'H264')
        out = cv2.VideoWriter(output_file, fourcc, target_fps, (target_width, target_height))
        
        if not out.isOpened():
            # Try alternative codec
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            out = cv2.VideoWriter(output_file, fourcc, target_fps, (target_width, target_height))
            
            if not out.isOpened():
                print("ERROR: Could not open output video writer")
                cap.release()
                return False
        
        frame_count = 0
        processed_frames = 0
        frame_skip = max(1, int(fps / target_fps))
        
        print(f"Processing every {frame_skip} frames...")
        
        while cap.isOpened() and processed_frames < max_frames:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Skip frames more aggressively
            if frame_count % frame_skip == 0:
                # Resize frame
                if width != target_width or height != target_height:
                    frame = cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_AREA)
                
                # Additional compression: reduce quality slightly
                # This simulates lower bitrate by slightly blurring
                frame = cv2.GaussianBlur(frame, (1, 1), 0)
                
                # Write the frame
                out.write(frame)
                processed_frames += 1
                
                # Show progress
                if processed_frames % 25 == 0:
                    progress = (processed_frames / max_frames) * 100
                    print(f"  Progress: {progress:.1f}% ({processed_frames}/{max_frames} frames)")
            
            frame_count += 1
        
        # Release everything
        cap.release()
        out.release()
        
        # Check file sizes
        if os.path.exists(output_file):
            original_size = os.path.getsize(input_file) / (1024 * 1024)  # MB
            compressed_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            print(f"\nCompression complete!")
            print(f"Original size: {original_size:.1f} MB")
            print(f"Compressed size: {compressed_size:.1f} MB")
            
            if compressed_size < original_size:
                print(f"Size reduction: {compression_ratio:.1f}%")
                
                # If we got good compression, offer to replace
                if compressed_size < 50:  # If under 50MB, that's acceptable
                    print(f"\nReplacing original file with compressed version...")
                    os.remove(input_file)
                    os.rename(output_file, input_file)
                    print("Original file replaced with compressed version.")
                    return True
                else:
                    print("File is still quite large. Consider manual compression.")
                    return True
            else:
                print(f"File size increased by {-compression_ratio:.1f}%")
                print("Compression was not effective with these settings.")
                return False
        else:
            print("ERROR: Compressed file was not created")
            return False
            
    except Exception as e:
        print(f"Error during compression: {e}")
        return False

if __name__ == "__main__":
    print("Aggressive Video Compression Tool")
    print("=" * 35)
    
    success = compress_video()
    
    if success:
        print("\nVideo compression completed successfully!")
        print("You can now enable the video background on the news page.")
    else:
        print("\nVideo compression was not effective.")
        print("Consider using online compression tools for better results.")