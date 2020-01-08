from bitstring import Bits

from structure.Blob import Blob
from structure.Blobs import Blobs
from structure.Image import Image
from structure.Vector import Vector2


def loadBlobsInformation(filename: str) -> (Blobs, Vector2):
    with open(filename, "rb") as f:
        sizeX: int = int.from_bytes(f.read(4), byteorder="big", signed=False)
        sizeY: int = int.from_bytes(f.read(4), byteorder="big", signed=False)
        size = Vector2(sizeX, sizeY)

        blobs = []
        for posY in range(0, sizeY):
            blobsRow = []
            for posX in range(0, sizeX):
                blobData = f.read(1)
                blobDataBits = Bits(blobData)
                blobsRow.append(Blob.fromBits(blobDataBits, Vector2(posX, posY), Vector2(8, 8)))
            blobs.append(blobsRow)

        blobs = Blobs.fromBlobsList(blobs)
        return blobs, size


def connectBlobsByReferences(blobs: Blobs):
    for blob in blobs.blobs:





def main(blobs_image_path: str, blobs_info_path: str, output_path: str):
    blobsList, size = loadBlobsInformation(blobs_info_path)
    blobs: Blobs = Blobs.fromBlobsList(blobsList)
    blobs.


    print("Decompression [DONE]")


if __name__ == '__main__':
    main("temp/saved_blobs.jpg", "temp/saved_data.pcf", "temp/saved_decompressed.jpg")
