import numpy as np
from PIL import ImageChops, Image as PilImage

from image_manipulation import show_image_from_numpy_array, calculate_difference_in_images
from structure.Blob import TYPES, ROTATIONS
from structure.Image import Image
from structure.Vector import Vector2


def main(load_path: str, save_path: str):
    image: Image = Image.fromFile(load_path, Vector2(8, 8))
    print(f"blobs size: {image.blobs.size}")
    image.showFromBlobs("Blobs")

    blob0 = image.blobs.get(0, 0)
    blob1 = image.blobs.get(30, 10)

    pixels0 = blob0.getPixels()
    pixels1 = blob1.getPixels()

    show_image_from_numpy_array(pixels0, "pixels0")
    show_image_from_numpy_array(pixels1, "pixels1")

    diff = calculate_difference_in_images(pixels0, pixels1)
    print(f"Diff: {diff}")

    # image.showFromBlobs("Derivated")
    print("Compression [DONE]")


if __name__ == '__main__':
    main("../testing_data/white.bmp", "temp/andrea-ultra-compressed.pca")
