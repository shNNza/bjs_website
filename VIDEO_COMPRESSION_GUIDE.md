# Video Compression Guide for News Page Background

## Video Requirements
- Place your video files in: `website/static/website/videos/`
- Recommended filenames: `news-background.mp4` and `news-background.webm`

## Compression Settings for Web Optimization

### For MP4 (H.264):
```bash
ffmpeg -i input_video.mp4 -c:v libx264 -preset slow -crf 28 -c:a aac -b:a 128k -vf "scale=1920:1080" news-background.mp4
```

### For WebM (VP9):
```bash
ffmpeg -i input_video.mp4 -c:v libvp9 -b:v 1M -c:a libvorbis -b:a 128k -vf "scale=1920:1080" news-background.webm
```

## Key Parameters:
- **Resolution**: 1920x1080 (Full HD is sufficient for backgrounds)
- **CRF 28**: Good balance between quality and file size
- **Bitrate**: ~1Mbps for background videos
- **Audio**: 128k AAC/Vorbis (though video will be muted)

## File Size Goals:
- Target: Under 5MB for 10-15 second loops
- Maximum: Under 10MB for longer clips

## Current Implementation:
- Video plays automatically, muted, and loops continuously
- Blue overlay applied with same colors as hero banner: `rgba(30, 60, 114, 0.6)` to `rgba(42, 82, 152, 0.6)`
- Fallback gradient background if video fails to load
- Responsive design for mobile devices