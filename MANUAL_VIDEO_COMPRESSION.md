# Manual Video Compression Guide

Your video file `news-background.mp4` is currently **247MB**, which is too large for web use.

## 🎯 Target Size
- **Ideal**: 5-10MB for background videos
- **Maximum**: 20MB for acceptable loading times

## 🔧 Compression Options

### Option 1: Online Video Compressors (Easiest)
1. **CloudConvert** (https://cloudconvert.com/mp4-converter)
   - Upload your video
   - Set quality to "Medium" or "Low"
   - Set resolution to 1920x1080 (if higher)
   - Download compressed version

2. **Online-Convert** (https://www.online-convert.com/compress-video)
   - Similar process, good compression options

### Option 2: VLC Media Player (Free Desktop Tool)
1. Open VLC → Media → Convert/Save
2. Add your video file
3. Click "Convert/Save"
4. Profile: Choose "Video - H.264 + MP3 (MP4)"
5. Click Settings (wrench icon):
   - Video: Bitrate 1000 kb/s, Frame Rate 24
   - Audio: Bitrate 128 kb/s
   - Resolution: 1920x1080 max
6. Choose output file: `news-background-compressed.mp4`
7. Start conversion

### Option 3: FFmpeg Command Line (If Available)
```bash
# Install ffmpeg first, then run:
ffmpeg -i news-background.mp4 -c:v libx264 -crf 28 -preset medium -vf "scale=1920:1080" -c:a aac -b:a 128k -t 30 news-background-compressed.mp4
```

### Option 4: Windows Built-in Tools
1. **Photos App**:
   - Right-click video → Open with → Photos
   - Click "Edit & Create" → "Create a video with text"
   - Export with lower quality settings

## 📐 Recommended Settings
- **Resolution**: 1920x1080 (Full HD)
- **Bitrate**: 1000-1500 kbps
- **Frame Rate**: 24 fps
- **Duration**: 15-30 seconds (loops well)
- **Format**: MP4 (H.264)

## 🔄 After Compression
1. Replace the original file with compressed version
2. Rename it to `news-background.mp4`
3. The website will automatically use it

## 🧪 Testing
Once compressed, test the video loads quickly by:
1. Refreshing the news page
2. Checking browser developer tools → Network tab
3. Video should load in under 3-5 seconds

## 📝 Current Status
- ❌ Original: 247MB (too large)
- ⏳ Target: 5-10MB (90-95% compression needed)
- 🎯 Goal: Fast loading background video