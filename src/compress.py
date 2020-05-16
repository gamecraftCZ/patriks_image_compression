import copy
import os

import numpy as np

from bitstring import Bits

from image_manipulation import save_image_from_numpy_array
from structure.Blob import TYPES, ROTATIONS
from structure.Blobs import Blobs
from structure.Image import Image
from structure.Vector import Vector2

# Image resolution must be dividable by blockSize in both axises
# Image resolution must be a least 8 times the blockSize
DIFF_THRESHOLD = 50_000


def getBestRotationWithDif(blob, blobToCompare):
    diffNone = blob.diff(blobToCompare, ROTATIONS.NONE)
    diffRight = blob.diff(blobToCompare, ROTATIONS.RIGHT)
    diffLeft = blob.diff(blobToCompare, ROTATIONS.LEFT)
    diffDown = blob.diff(blobToCompare, ROTATIONS.DOWN)

    minDiff = min(diffNone, diffRight, diffDown, diffLeft)
    if minDiff == diffNone:
        return minDiff, ROTATIONS.NONE
    if minDiff == diffRight:
        return minDiff, ROTATIONS.RIGHT
    if minDiff == diffLeft:
        return minDiff, ROTATIONS.LEFT
    if minDiff == diffDown:
        return minDiff, ROTATIONS.DOWN


def runCompressionRound(allBlobs: list, progressObject=None):
    if progressObject is None:
        progressObject = {"count": 0, "max": len(allBlobs), "cancel": False}
    for blob in allBlobs:
        if progressObject.get("cancel"):
            return
        progressObject["count"] += 1
        print(f'Blobs tested: {progressObject["count"]} / {progressObject["max"]}')
        for blobToCompare in blob.getBlobsAroundFlattened():
            if blob.position == blobToCompare.position:
                continue
            diff, rotation = getBestRotationWithDif(blob, blobToCompare)
            if diff < DIFF_THRESHOLD:
                # print(f"Diff: {diff}")
                if not blobToCompare.checkIfReferencedInDerivations(blob) and diff < blob.lowestDerivation:
                    # print("Derivating")
                    blob.setDerivation(blobToCompare, rotation)

    derivatedBlocks = 0
    for blob in allBlobs:
        if blob.derivatedFromBlob:
            derivatedBlocks += 1
    print(f"Derived Blocks: {derivatedBlocks}")


def saveJustBlobs(blobsList: list, filename: str) -> Blobs:
    fixedBlobs = []
    for blob in blobsList:
        if blob.type == TYPES.FIXED:
            blob = copy.copy(blob)
            blob.position = Vector2(len(fixedBlobs), 0)
            fixedBlobs.append(blob)

    blobsList: Blobs = Blobs(np.zeros((0, 0)), Vector2(8, 8))

    blobsList.blobs = [fixedBlobs]
    # Size is in blobs count
    blobsList.size.x = len(fixedBlobs)
    blobsList.size.y = 1
    blobsList.raw_pixels_resolution = Vector2(len(fixedBlobs) * 8, 8)

    save_image_from_numpy_array(filename, blobsList.toPixels(), 70)
    return blobsList


def saveBlobsInformation(blobs: Blobs, filename: str):
    headers: Bits = blobs.headersToBits()
    with open(filename, "wb+") as f:
        # Size is in blobs count
        f.write(blobs.size.x.to_bytes(4, byteorder="big", signed=False))
        f.write(blobs.size.y.to_bytes(4, byteorder="big", signed=False))
        f.write(headers.bytes)



def main(load_path: str, uncompressed_save_path: str,
         save_path_image: str, save_path_data: str):
    image: Image = Image.fromFile(load_path, Vector2(8, 8))
    image.saveFile(uncompressed_save_path)
    image.saveFile(uncompressed_save_path.replace(".jpg", ".png"))
    image.saveFile(uncompressed_save_path.replace(".jpg", ".bmp"))

    print(f"blobs size: {image.blobs.size}")
    image.showFromBlobs("Blobs")

    allBlobs = image.getFlattenedBlobsArray()
    runCompressionRound(allBlobs)
    print("FINISHED round 1")


    ## SAVE ##
    saveBlobsInformation(image.blobs, save_path_data)
    saveJustBlobs(allBlobs, save_path_image)
    saveJustBlobs(allBlobs, save_path_image.replace(".jpg", ".png"))
    saveJustBlobs(allBlobs, save_path_image.replace(".jpg", ".bmp"))

    image.showFromBlobs("Derived")

    image.showFromBlobsWithWhites("Derived")
    # image.saveFileWithWhites(save_path)

    print("Compression [DONE]")


if __name__ == '__main__':
    main("../testing_data/andrea-low-res.jpg", "temp/andrea_uncompressed.jpg",
         "temp/saved_blobs.jpg", "temp/saved_data.pcf")
