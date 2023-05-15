import cv2
import subprocess as sp
import numpy as np

# Set up capture device for video
cap = cv2.VideoCapture(0)

# Set up subprocess for FFmpeg
ffmpeg_cmd = [
    "ffmpeg",
    "-f", "rawvideo",
    "-pixel_format", "bgr24",
    "-video_size", "640x480",
    "-framerate", "30",
    "-i", "-",
    "-f", "dshow",
    "-i", "audio=Microphone Array (Realtek(R) Audio)",
    "-c:v", "libx264",
    "-preset", "ultrafast",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-ar", "44100",
    "-f", "flv", "rtmp://192.168.58.54/live/stream1"
]
ffmpeg = sp.Popen(ffmpeg_cmd, stdin=sp.PIPE)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        break

    # Write frame to FFmpeg subprocess
    ffmpeg.stdin.write(frame.tobytes())

# ffmpeg -list_devices true -f dshow -i dummy