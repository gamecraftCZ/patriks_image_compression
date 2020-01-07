import numpy as np
from PIL import Image, ImageChops
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


def calculate_difference_in_images(image1: np.ndarray, image2: np.ndarray) -> int:
    diff_image = ImageChops.difference(Image.fromarray(image1), Image.fromarray(image2))
    diff_array = np.array(diff_image).flatten()
    return (diff_array ** 2).sum()
