from image_manipulation import load_image_to_numpy_array, save_image_from_numpy_array, show_image_from_numpy_array
from structure.Blob import generateBlobsArrayFromImage, convertBlobsToImage, Blobs
from structure.Vector import Vector2


def main():
    # test load and save
    image = load_image_to_numpy_array("../../testing_data/andrea-ultra-low-res.bmp")

    blobs = Blobs(image, Vector2(8, 8))
    # for y in range(0, blobs.size.y):
    #     for x in range(0, blobs.size.x):
    #         show_image_from_numpy_array(blobs.get(x, y).pixels, f"{Vector2(x, y)}")

    img = convertBlobsToImage(blobs)

    show_image_from_numpy_array(img)
    save_image_from_numpy_array("temp/andrea-low-res-successful-save.bmp", img)


if __name__ == '__main__':
    main()
