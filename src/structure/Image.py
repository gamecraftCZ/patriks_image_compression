import numpy as np

from image_manipulation import show_image_from_numpy_array
from structure.Blob import generateBlobsArrayFromImage, convertBlobsToImage, Blobs
from structure.Vector import Vector2


class Image:
    pixels: np.ndarray
    blobs: Blobs
    size: Vector2

    def __init__(self, pixels: np.ndarray, blobSize: Vector2):
        self.pixels = pixels
        self.blobs = Blobs(pixels, blobSize)
        self.size = Vector2(pixels.shape[1], pixels.shape[0])

    def show(self, title: str = ""):
        show_image_from_numpy_array(self.pixels, title)

    def showFromBlobs(self, title: str = ""):
        image = convertBlobsToImage(self.blobs)
        show_image_from_numpy_array(image, title)

