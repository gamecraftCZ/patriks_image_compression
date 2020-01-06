import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def load_image_to_numpy_array(filename: str) -> np.ndarray:
    img = Image.open(filename)
    arr = np.array(img)
    return arr


def save_image_from_numpy_array(filename: str, image_array: np.ndarray):
    img = Image.fromarray(image_array)
    img.save(filename)


def show_image_from_numpy_array(image_array: np.ndarray, header: str = "", axis: bool = False):
    fig, ax = plt.subplots()
    ax.set_title(header)
    ax.imshow(image_array)

    if not axis:
        plt.axis("off")

    plt.show()
