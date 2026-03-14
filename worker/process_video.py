import sys
import subprocess
import os
import shutil
import cv2
import numpy as np
from PIL import Image
from rembg import remove, new_session

video = sys.argv[1]

ffmpeg = r"C:\Users\KIIT\Downloads\ffmpeg-master-latest-win64-gpl-shared\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"

frames_dir = "frames"
processed_dir = "processed"

# clean previous runs
if os.path.exists(frames_dir):
    shutil.rmtree(frames_dir)

if os.path.exists(processed_dir):
    shutil.rmtree(processed_dir)

os.makedirs(frames_dir)
os.makedirs(processed_dir)

print("Extracting frames...")

subprocess.call([
    ffmpeg,
    "-i", video,
    "-vf", "fps=30",
    f"{frames_dir}/frame_%04d.png"
])

print("Loading AI model...")

session = new_session("u2net_human_seg")

frames = sorted(os.listdir(frames_dir))

print("Processing frames...")

for frame_name in frames:

    frame_path = os.path.join(frames_dir, frame_name)

    img = Image.open(frame_path).convert("RGBA")

    result = remove(img, session=session)

    result_np = np.array(result)

    # ensure alpha channel exists
    if result_np.shape[2] == 3:
        alpha = np.zeros((result_np.shape[0], result_np.shape[1]), dtype=np.uint8)
        result_np = np.dstack((result_np, alpha))

    # smooth alpha edges
    alpha = result_np[:, :, 3]
    alpha = cv2.GaussianBlur(alpha, (5,5), 0)
    result_np[:, :, 3] = alpha

    Image.fromarray(result_np).save(os.path.join(processed_dir, frame_name))

print("Rebuilding transparent video...")

subprocess.call([
    ffmpeg,
    "-framerate","30",
    "-i",f"{processed_dir}/frame_%04d.png",
    "-c:v","libvpx-vp9",
    "-pix_fmt","yuva420p",
    "../outputs/output.webm"
])

print("Done")
