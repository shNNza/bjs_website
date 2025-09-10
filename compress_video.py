#!/usr/bin/env python3
"""
Video compression script for web optimization
Compresses the news background video to reduce file size for web use
"""

import os
from moviepy.editor import VideoFileClip

def compress_video():
    video_dir = "website/static/website/videos/"
    input_file = os.path.join(video_dir, "news-background.mp4")
    output_file = os.path.join(video_dir, "news-background-compressed.mp4")
    
    print(f"Compressing video: {input_file}")
    print("This may take a few minutes...")
    
    try:
        # Load the video
        video = VideoFileClip(input_file)
        
        # Get video info
        print(f"Original duration: {video.duration:.2f} seconds")
        print(f"Original resolution: {video.w}x{video.h}")
        print(f"Original FPS: {video.fps}")
        
        # For background videos, we can:
        # 1. Reduce resolution to 1920x1080 if higher
        # 2. Reduce quality/bitrate
        # 3. Limit duration if it's very long (background videos work well as loops)
        
        # Determine target resolution
        target_width = min(1920, video.w)
        target_height = int(target_width * video.h / video.w)
        
        # If video is longer than 30 seconds, we might want to trim it
        # Background videos work well as short loops
        max_duration = min(30, video.duration)  # Max 30 seconds
        
        print(f"Target resolution: {target_width}x{target_height}")
        print(f"Target duration: {max_duration:.2f} seconds")
        
        # Process the video
        processed_video = video.subclip(0, max_duration)
        
        # Resize if needed
        if target_width != video.w or target_height != video.h:
            processed_video = processed_video.resize((target_width, target_height))
        
        # Write the compressed video
        # Using lower bitrate for web optimization
        processed_video.write_videofile(
            output_file,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            bitrate='1000k',  # 1 Mbps - good for background videos
            fps=24  # Standard web video fps
        )
        
        # Clean up
        video.close()
        processed_video.close()
        
        # Check file sizes
        original_size = os.path.getsize(input_file) / (1024 * 1024)  # MB
        compressed_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        print(f"\n✅ Compression complete!")
        print(f"Original size: {original_size:.1f} MB")
        print(f"Compressed size: {compressed_size:.1f} MB")
        print(f"Size reduction: {compression_ratio:.1f}%")
        print(f"Compressed video saved as: {output_file}")
        
        # If compression was successful and significant, offer to replace original
        if compressed_size < original_size * 0.8:  # If at least 20% reduction
            replace = input("\nReplace original file with compressed version? (y/n): ").lower().strip()
            if replace == 'y':
                os.remove(input_file)
                os.rename(output_file, input_file)
                print("✅ Original file replaced with compressed version.")
            else:
                print("Compressed file kept as separate file.")
        
    except Exception as e:
        print(f"❌ Error during compression: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🎬 Video Compression Tool")
    print("=" * 30)
    
    # Check if the video file exists
    video_path = "website/static/website/videos/news-background.mp4"
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        print("Please make sure the video file is in the correct location.")
    else:
        compress_video()
    
    print("\n🎉 Done!")