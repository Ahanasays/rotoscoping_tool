import os
import sys
import cv2
import subprocess
from rembg import remove
from PIL import Image

video = sys.argv[1]

frames_dir = "frames"
processed_dir = "processed"

os.makedirs(frames_dir, exist_ok=True)
os.makedirs(processed_dir, exist_ok=True)

print("Extracting frames...")

subprocess.call([
    r"C:\Users\KIIT\Downloads\ffmpeg-master-latest-win64-gpl-shared\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe",
    "-i", video,
    f"{frames_dir}/frame_%04d.png"
])

print("Running rotoscope AI...")

for frame in os.listdir(frames_dir):

    path = os.path.join(frames_dir, frame)

    with open(path, "rb") as f:
        input_data = f.read()

    output = remove(input_data)

    with open(os.path.join(processed_dir, frame), "wb") as out:
        out.write(output)

print("Rebuilding video...")

subprocess.call([
    r"C:\Users\KIIT\Downloads\ffmpeg-master-latest-win64-gpl-shared\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe",
    "-framerate", "30",
    "-i", f"{processed_dir}/frame_%04d.png",
    "-pix_fmt", "yuva420p",
    "../outputs/output.mov"
])

print("Done")
