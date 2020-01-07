from structure.Blob import TYPES, ROTATIONS
from structure.Image import Image
from structure.Vector import Vector2


def main(load_path: str, save_path: str):
    image: Image = Image.fromFile(load_path, Vector2(8, 8))
    image.showFromBlobs("Blobs")

    startBlob = image.blobs.get(0, 0)

    derivatorBlob = image.blobs.get(1, 1)
    derivatorBlob.type = TYPES.DERIVATED
    derivatorBlob.derivatedFromBlob = startBlob
    derivatorBlob.rotation = ROTATIONS.LEFT
    image.showFromBlobs("Derivated")


if __name__ == '__main__':
    main("../testing_data/andrea-ultra-low-res.jpg", "temp/andrea-ultra-compressed.pca")
