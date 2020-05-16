import numpy as np
import cv2
from image_manipulation import show_image_from_numpy_array, load_image_to_numpy_array, save_image_from_numpy_array
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

    def pixelsFromBlobs(self):
        return self.blobs.toPixels()

    def pixelsFromBlobsWithWhites(self):
        return self.blobs.toPixelsWithWhites()

    def showFromBlobsWithWhites(self, title: str = ""):
        show_image_from_numpy_array(self.pixelsFromBlobsWithWhites(), title)

    def saveFile(self, filename: str):
        save_image_from_numpy_array(filename, self.pixelsFromBlobs())

    def saveFileWithWhites(self, filename: str):
        save_image_from_numpy_array(filename, self.pixelsFromBlobsWithWhites())


    def getFlattenedBlobsArray(self) -> list:
        blobs = []
        for blob_row in self.blobs.blobs:
            for blob in blob_row:
                blobs.append(blob)
        return blobs

    @staticmethod
    def fromFile(filename: str, blobSize: Vector2):
        pixels = load_image_to_numpy_array(filename)
        pixels = cv2.resize(pixels, dsize=(pixels.shape[0] // 8 * 8, pixels.shape[1] // 8 * 8))
        return Image(pixels, blobSize)
