from image_manipulation import load_image_to_numpy_array, save_image_from_numpy_array, show_image_from_numpy_array
from structure.Vector import Vector2


def main(load_path: str, save_path: str):
    image = load_image_to_numpy_array(load_path)
    show_image_from_numpy_array(image, "Original")

    resolution = Vector2(image.shape[0], image.shape[1])
    blobs = Vector2(8, 8)


if __name__ == '__main__':
    main("../testing_data/andrea-low-res.jpg", "temp/andrea-compressed.pca")
