import numpy as np
from PIL import ImageChops, Image as PilImage

from image_manipulation import show_image_from_numpy_array, calculate_difference_in_images
from structure.Blob import TYPES, ROTATIONS
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

def run_compression_round(allBlobs: list):
    blobsTested = 0
    blobsCount = len(allBlobs)
    for blob in allBlobs:
        blobsTested += 1
        print(f"Blobs tested: {blobsTested} / {blobsCount}")
        for blobToCompare in blob.getBlobsAround():
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
    print(f"derivatedBlocks: {derivatedBlocks}")


def main(load_path: str, save_path: str):
    image: Image = Image.fromFile(load_path, Vector2(8, 8))
    print(f"blobs size: {image.blobs.size}")
    image.showFromBlobs("Blobs")

    allBlobs = image.getFlattenedBlobsArray()

    run_compression_round(allBlobs)
    print("FINSHED round 1")

    # run_compression_round(allBlobs)
    # print("FINSHED round 2")
    #
    # run_compression_round(allBlobs)
    # print("FINSHED round 3")


    image.showFromBlobs("Derivated")
    print("Compression [DONE]")


if __name__ == '__main__':
    main("../testing_data/andrea-low-res.bmp", "temp/andrea-ultra-compressed.pca")
