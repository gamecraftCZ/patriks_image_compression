from enum import Enum

import numpy as np
from bitstring import BitStream, BitArray, Bits

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

    @staticmethod
    def fromInt(number: int) -> "ROTATIONS":
        if number == 1:
            return ROTATIONS.RIGHT
        if number == 2:
            return ROTATIONS.LEFT
        if number == 3:
            return ROTATIONS.DOWN

        return ROTATIONS.NONE


class Blob:
    type: TYPES = TYPES.FIXED

    derivatedFromBlob: "Blob" = None
    _derivedPositionFromBitsParse: Vector2
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

    def getPixelsOrWhiteIfNotDerived(self) -> np.ndarray:
        if self.type == TYPES.FIXED:
            return self._pixels
        else:
            return np.zeros(shape=self.size.asTupleWithArgs((3,)), dtype="uint8")

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

    def _getLeftestDerivationPosition(self):
        leftestPosition = self.position.x - self.size.x // 2

        if leftestPosition < 0:
            leftestPosition = 0
        elif leftestPosition + self.size.x >= self.blobsObject.size.x:
            leftestPosition = self.blobsObject.size.x - self.size.x

        return leftestPosition

    def _getToppestDerivationPosition(self):
        toppestPosition = self.position.y - self.size.y // 2

        if toppestPosition < 0:
            toppestPosition = 0
        elif toppestPosition + self.size.y >= self.blobsObject.size.y:
            toppestPosition = self.blobsObject.size.y - self.size.y

        return toppestPosition


    def getBlobsAround(self) -> list:
        leftestPosition = self._getLeftestDerivationPosition()
        toppestPosition = self._getToppestDerivationPosition()

        blobsAround = self.blobsObject.blobs[toppestPosition: toppestPosition + 8]
        blobsAround = [row[leftestPosition:leftestPosition+8] for row in blobsAround]
        blobsAroundFlattened = [item for sublist in blobsAround for item in sublist if item is not self]
        return blobsAroundFlattened


    def diffRaw(self, anotherBlob: "Blob"):
        return calculate_difference_in_images(self._pixels, anotherBlob._pixels)


    def getDerivedPosition(self) -> (int, int):
        targetBlob = self.derivatedFromBlob or self

        leftestPosition = self._getLeftestDerivationPosition()
        toppestPosition = self._getToppestDerivationPosition()

        relativeDerivedX = targetBlob.position.x - leftestPosition
        relativeDerivedY = targetBlob.position.y - toppestPosition

        return relativeDerivedX, relativeDerivedY


    def __str__(self):
        # P is position
        # D is derived blob position
        derivedPosition = "None"
        if self.derivatedFromBlob:
            derivedPosition = self.derivatedFromBlob.position
            derivedPosition = f"D(x:{derivedPosition.x},y:{derivedPosition.y})"
        elif self._derivedPositionFromBitsParse:
            derivedPosition = self._derivedPositionFromBitsParse
            derivedPosition = f"D?(x:{derivedPosition.x},y:{derivedPosition.y})"

        return f"P(x:{self.position.x},y:{self.position.y}) {derivedPosition}"


    def headerToBits(self) -> Bits:
        bitString = ""

        # Save derived position
        posX, posY = self.getDerivedPosition()
        bitString += f"{posX:03b} "
        bitString += f"{posY:03b} "

        # Save rotation
        bitString += f"{self.rotation.value:02b} "

        # Convert to BitArray
        # print(bitString)
        return Bits(bin=bitString)


    @staticmethod
    def fromBits(bits: Bits, position: Vector2, size: Vector2) -> "Blob":
        blob = Blob(np.empty((8, 8, 3), dtype="uint8"), position)
        blob.position = position
        blob.size = size

        # Load info from bits
        derivedX = bits[0:3].uint
        derivedY = bits[3:6].uint
        blob._derivedPositionFromBitsParse = Vector2(derivedX, derivedY)

        rotationInt = bits[6:8].uint
        blob.rotation = ROTATIONS.fromInt(rotationInt)

        return blob




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
