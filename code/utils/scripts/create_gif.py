import os
import sys

from PIL import Image
from images2gif import writeGif

# This script generates a gif file from a folder containing single frames in png format.
# Usage example:
#    > python create_gif.py path/to/your/animation.gif path/to/the/frames
if __name__ == '__main__':
    gif_path = sys.argv[1]
    frames_path = sys.argv[2]
    file_names = sorted((os.path.join(frames_path, fn) for fn in os.listdir(frames_path) if fn.endswith('.png')))
    images = [Image.open(fn) for fn in file_names]
    writeGif(gif_path, images, duration=0.1)
