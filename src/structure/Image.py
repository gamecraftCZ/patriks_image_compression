import numpy as np

from image_manipulation import show_image_from_numpy_array, load_image_to_numpy_array
from structure.Blobs import Blobs, convertBlobsToImage
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
        image = self.blobs.toPixels()
        show_image_from_numpy_array(image, title)

    def getFlattenedBlobsArray(self) -> list:
        blobs = []
        for blob_row in self.blobs.blobs:
            for blob in blob_row:
                blobs.append(blob)
        return blobs

    @staticmethod
    def fromFile(filename: str, blobSize: Vector2):
        pixels = load_image_to_numpy_array(filename)
        return Image(pixels, blobSize)
