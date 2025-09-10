#!/usr/bin/env python3
"""
Simple video compression script using OpenCV
Compresses the news background video to reduce file size for web use
"""

import cv2
import os
import sys

def compress_video():
    video_dir = "website/static/website/videos/"
    input_file = os.path.join(video_dir, "news-background.mp4")
    output_file = os.path.join(video_dir, "news-background-compressed.mp4")
    
    if not os.path.exists(input_file):
        print(f"ERROR: Video file not found: {input_file}")
        return False
    
    print(f"Compressing video: {input_file}")
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
        print(f"  Total frames: {total_frames}")
        
        # Set target parameters for web optimization
        target_fps = min(24, fps)  # Max 24 fps for web
        target_width = min(1920, width)  # Max 1920px width
        target_height = int(target_width * height / width)  # Maintain aspect ratio
        
        # Limit duration to 30 seconds for background videos
        max_duration = min(30, duration)
        max_frames = int(max_duration * target_fps)
        
        print(f"Target video info:")
        print(f"  Resolution: {target_width}x{target_height}")
        print(f"  FPS: {target_fps}")
        print(f"  Duration: {max_duration:.2f} seconds")
        print(f"  Frames to process: {max_frames}")
        
        # Define the codec and create VideoWriter
        # Using H.264 codec with lower quality for smaller file size
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, target_fps, (target_width, target_height))
        
        if not out.isOpened():
            print("ERROR: Could not open output video writer")
            cap.release()
            return False
        
        frame_count = 0
        processed_frames = 0
        
        print("Processing frames...")
        
        while cap.isOpened() and processed_frames < max_frames:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Skip frames to reduce file size (keep every nth frame based on fps reduction)
            if frame_count % max(1, int(fps / target_fps)) == 0:
                # Resize frame if needed
                if width != target_width or height != target_height:
                    frame = cv2.resize(frame, (target_width, target_height))
                
                # Write the frame
                out.write(frame)
                processed_frames += 1
                
                # Show progress
                if processed_frames % 50 == 0:
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
            print(f"Size reduction: {compression_ratio:.1f}%")
            print(f"Compressed video saved as: {output_file}")
            
            # If compression was successful and significant, offer to replace original
            if compressed_size < original_size * 0.8 and compressed_size < 20:  # If at least 20% reduction and under 20MB
                print(f"\nReplacing original file with compressed version...")
                os.remove(input_file)
                os.rename(output_file, input_file)
                print("Original file replaced with compressed version.")
                return True
            else:
                print("Compressed file kept as separate file.")
                return True
        else:
            print("ERROR: Compressed file was not created")
            return False
            
    except Exception as e:
        print(f"Error during compression: {e}")
        return False

if __name__ == "__main__":
    print("OpenCV Video Compression Tool")
    print("=" * 35)
    
    success = compress_video()
    
    if success:
        print("\nVideo compression completed successfully!")
        print("You can now enable the video background on the news page.")
    else:
        print("\nVideo compression failed.")
        print("Please try manual compression using the guide provided.")