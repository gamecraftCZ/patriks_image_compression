from bitstring import Bits

from image_manipulation import show_image_from_numpy_array, load_image_to_numpy_array, save_image_from_numpy_array
from structure.Blob import Blob, TYPES
from structure.Blobs import Blobs
from structure.Image import Image
from structure.Vector import Vector2


def loadBlobsInformation(filename: str) -> Blobs:
    with open(filename, "rb") as f:
        sizeX: int = int.from_bytes(f.read(4), byteorder="big", signed=False)
        sizeY: int = int.from_bytes(f.read(4), byteorder="big", signed=False)

        blobs = []
        for posY in range(0, sizeY):
            blobsRow = []
            for posX in range(0, sizeX):
                blobData = f.read(1)
                blobDataBits = Bits(blobData)
                blobsRow.append(Blob.fromBits(blobDataBits, Vector2(posX, posY), Vector2(8, 8)))
            blobs.append(blobsRow)

        blobs = Blobs.fromBlobsList(blobs)
        return blobs


def loadBlobsPixels(blobs: Blobs, filename: str):
    image = load_image_to_numpy_array(filename)
    xPositionInImage = 0
    for blob in blobs.getFlattenedBlobsArray():
        if blob.type == TYPES.FIXED:
            pixels = image[0:8, xPositionInImage:xPositionInImage+8]
            blob._pixels = pixels
            xPositionInImage += 8


def main(blobs_image_path: str, blobs_info_path: str, output_path: str):
    # image: Image = Image.fromFile(blobs_image_path, Vector2(8, 8))
    # image.showFromBlobs()

    # LOAD
    blobs: Blobs = loadBlobsInformation(blobs_info_path)
    loadBlobsPixels(blobs, blobs_image_path)

    # SHOW
    image = blobs.toPixels()
    show_image_from_numpy_array(image, "decompressed")
    save_image_from_numpy_array(output_path, image)

    print("Decompression [DONE]")


if __name__ == '__main__':
    main("temp/saved_blobs.png", "temp/saved_data.pcf", "temp/saved_decompressed.png")
