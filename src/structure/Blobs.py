import numpy as np
from bitstring import Bits

from structure.Blob import Blob
from structure.Vector import Vector2


class Blobs:
    blobs: list = []
    size: Vector2 = Vector2(0, 0)
    raw_pixels_resolution: Vector2 = Vector2(0, 0)

    # Blob size must be x and y the same
    def __init__(self, pixels: np.ndarray, blobSize: Vector2):
        if pixels.size == 0:
            return

        self.blobs = generateBlobsArrayFromImage(pixels, blobSize)
        # Set reference to this list of blobs for decompression purposes, so they can address each other
        for blobs_row in self.blobs:
            for blob in blobs_row:
                blob.blobsObject = self

        self.size = Vector2(len(self.blobs[0]), len(self.blobs))
        self.raw_pixels_resolution = Vector2(pixels.shape[1], pixels.shape[0])

    def get(self, x, y) -> Blob:
        return self.blobs[y][x]

    def toPixels(self):
        return convertBlobsToImage(self)

    def toPixelsWithWhites(self):
        return convertBlobsToImage(self, True)

    def getFlattenedBlobsArray(self) -> list:
        blobs = []
        for blob_row in self.blobs:
            for blob in blob_row:
                blobs.append(blob)
        return blobs

    def headersToBits(self) -> Bits:
        headerBits = Bits()
        for blob in self.getFlattenedBlobsArray():
            headerBits += blob.headerToBits()
        return headerBits


    @staticmethod
    def fromBlobsList(blobs: list) -> "Blobs":
        blobsObj = Blobs(np.empty((0, 0)), None)
        blobsObj.blobs = blobs
        blobsObj.size = Vector2(len(blobs[0]), len(blobs))
        blobsObj.raw_pixels_resolution = blobsObj.size * Vector2(8, 8)

        for blobs_row in blobs:
            for blob in blobs_row:
                blob.blobsObject = blobsObj
                # print(f"fromBlobsList: {blob}")
                blob.setDerivedBlockFromDerivedPositionFromBitsParse()
        return blobsObj


# Image resolution must be dividable by blockSize in both axises
def generateBlobsArrayFromImage(pixels: np.ndarray, blobSize: Vector2) -> list:
    resolution = Vector2(pixels.shape[1], pixels.shape[0])

    blobs = []
    for y in range(0, resolution.y, blobSize.y):
        # Y axis
        blobsY = []
        for x in range(0, resolution.x, blobSize.x):
            # X axis
            blobPixels = pixels[y:y + 8, x:x + 8]
            blob = Blob(blobPixels, Vector2(x, y) / blobSize)
            blobsY.append(blob)

        blobs.append(blobsY)

    return blobs


def addBlobToPixelsArray(blob: Blob, pixelsArray: np.ndarray, whitesWhenDerived: bool = False):
    blobOffsetX = blob.position.x * blob.size.x
    blobOffsetY = blob.position.y * blob.size.y

    if whitesWhenDerived:
        blobPixels = blob.getPixelsOrWhiteIfNotDerived()
    else:
        blobPixels = blob.getPixels()

    for y in range(blob.size.y):
        for x in range(blob.size.x):
            pixelsArray[blobOffsetY+y, blobOffsetX+x] = blobPixels[y, x]

def convertBlobsToImage(blobs: Blobs, whitesWhenDerived: bool = False) -> np.ndarray:
    img: np.ndarray = np.empty((blobs.raw_pixels_resolution.y, blobs.raw_pixels_resolution.x, 3), dtype="uint8")
    for blobs_row in blobs.blobs:
        for blob in blobs_row:
            # print(f"convertBlobsToImage: {blob}")
            addBlobToPixelsArray(blob, img, whitesWhenDerived)

    return img
