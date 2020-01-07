from enum import Enum

import numpy as np

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

    derivatedFromBlob: "Blob"
    rotation: ROTATIONS = ROTATIONS.NONE

    position: Vector2
    size: Vector2
    pixels: np.ndarray

    def __init__(self, pixels: np.ndarray, position: Vector2):
        self.position = position.copy()
        self.size = Vector2(pixels.shape[1], pixels.shape[0])
        self.pixels = pixels

    def getPixels(self) -> np.ndarray:
        if self.type == TYPES.FIXED:
            return self.pixels
        else:
            # Derivated from another blob
            anotherBlobPixels = self.derivatedFromBlob.getPixels()
            if self.rotation == ROTATIONS.NONE:
                return anotherBlobPixels
            elif self.rotation == ROTATIONS.RIGHT:
                return np.rot90(anotherBlobPixels, 3)
            elif self.rotation == ROTATIONS.LEFT:
                return np.rot90(anotherBlobPixels)
            elif self.rotation == ROTATIONS.DOWN:
                return np.rot90(anotherBlobPixels, 2)
