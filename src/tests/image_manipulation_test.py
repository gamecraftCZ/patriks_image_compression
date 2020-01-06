from image_manipulation import load_image_to_numpy_array, save_image_from_numpy_array


def main():
    # test load and save
    image = load_image_to_numpy_array("../../testing_data/andrea-low-res.bmp")
    print(image.ndim)
    save_image_from_numpy_array("temp/andrea-low-res-successful-save.bmp", image)


if __name__ == '__main__':
    main()
