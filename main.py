import os
from PIL import Image
from CODE.image_stitching import unwrap_image
from CODE.product_info import ask_questions
from CODE.update_ui import run_ui

IMG_DIR = "./IMAGES"
VIDEO_DIR = "./VIDEOS"

# Example video name
video_name = "013.mp4"
img_name = f"{os.path.splitext(video_name)[0]}.png"
img_path = os.path.join(IMG_DIR, img_name)

# Uncomment for testing image unwrapping; set 'show=True' to visualize the video during processing
if img_name not in os.listdir(IMG_DIR):
    show = False  # Change to True for visualization
    unwrap_image(os.path.join(VIDEO_DIR, video_name), img_path, show)

img = Image.open(img_path)
base_name = os.path.basename(img_path)
ask_questions(img, base_name)
run_ui()