from enum import Enum

import numpy as np

from image_manipulation import calculate_difference_in_images
from structure.Vector import Vector2


class TYPES(Enum):
    FIXED = 0
    DERIVATED = 1


class ROTATIONS(Enum):
    NONE = 0
    RIGHT = 1
    LEFT = 2
    DOWN = 3


class Blob:
    type: TYPES = TYPES.FIXED

    derivatedFromBlob: "Blob" = None
    lowestDerivation: int = 9999999999999
    rotation: ROTATIONS = ROTATIONS.NONE

    position: Vector2
    size: Vector2
    _pixels: np.ndarray
    blobsObject: "Blobs" = None

    def __init__(self, pixels: np.ndarray, position: Vector2):
        self.position = position.copy()
        self.size = Vector2(pixels.shape[1], pixels.shape[0])
        self._pixels = pixels

    def getPixels(self) -> np.ndarray:
        if self.type == TYPES.FIXED:
            return self._pixels
        else:
            # This blob is derived from another blob
            anotherBlobPixels = self.derivatedFromBlob.getPixels()
            return Blob.rotateImage(anotherBlobPixels, self.rotation)

    def getOriginalDerivationSource(self) -> "Blob":
        if self.type == TYPES.FIXED:
            return self
        return self.derivatedFromBlob

    def checkIfReferencedInDerivations(self, anotherBlob: "Blob") -> bool:
        if self is anotherBlob:
            return True
        if self.derivatedFromBlob:
            return self.derivatedFromBlob.checkIfReferencedInDerivations(anotherBlob)
        return False

    def setDerivation(self, anotherBlob: "Blob", rotation: ROTATIONS):
        self.derivatedFromBlob = anotherBlob
        self.type = TYPES.DERIVATED
        self.rotation = rotation

    def diff(self, anotherBlob: "Blob", rotation: ROTATIONS = None):
        pixels = self._pixels
        if rotation:
            pixels = Blob.rotateImage(pixels, rotation)
        return calculate_difference_in_images(pixels, anotherBlob.getPixels())

    def getBlobsAround(self) -> list:
        leftestPosition = self.position.x - self.size.x // 2
        if leftestPosition < 0:
            leftestPosition = 0
        elif leftestPosition + self.size.x >= self.blobsObject.size.x:
            leftestPosition = self.blobsObject.size.x - self.size.x

        toppestPosition = self.position.y - self.size.y // 2
        if toppestPosition < 0:
            toppestPosition = 0
        elif toppestPosition + self.size.y >= self.blobsObject.size.y:
            toppestPosition = self.blobsObject.size.y - self.size.y

        blobsAround = self.blobsObject.blobs[toppestPosition: toppestPosition + 8]
        blobsAround = [row[leftestPosition:leftestPosition+8] for row in blobsAround]
        blobsAroundFlattened = [item for sublist in blobsAround for item in sublist if item is not self]
        return blobsAroundFlattened


    def diff_row(self, anotherBlob: "Blob"):
        return calculate_difference_in_images(self._pixels, anotherBlob._pixels)

    @staticmethod
    def rotateImage(pixels: np.ndarray, rotation: ROTATIONS) -> np.ndarray:
        if rotation == ROTATIONS.NONE:
            return pixels
        elif rotation == ROTATIONS.RIGHT:
            return np.rot90(pixels, 3)
        elif rotation == ROTATIONS.LEFT:
            return np.rot90(pixels)
        elif rotation == ROTATIONS.DOWN:
            return np.rot90(pixels, 2)