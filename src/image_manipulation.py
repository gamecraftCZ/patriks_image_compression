import numpy as np
from PIL import Image


def load_image_to_numpy_array(filename: str) -> np.ndarray:
    img = Image.open(filename)
    arr = np.array(img)
    return arr


def save_image_from_numpy_array(filename: str, image_array: np.ndarray):
    img = Image.fromarray(image_array)
    img.save(filename)
