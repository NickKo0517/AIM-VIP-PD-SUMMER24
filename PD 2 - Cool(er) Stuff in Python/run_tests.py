from generation_tests import *
import matplotlib.pyplot as plt

if __name__ == "__main__":
    unittest.main()

    """     view image generated    """
    # image = Image_Generator(image_size=50, name="testImg")
    # imgArray = image.generate_image(seed=randbits(128))
    # defaultPrint_opts = np.get_printoptions()
    # np.set_printoptions(precision=2)
    # print(imgArray[:10, :10])
    # plt.imsave("test_img.png", imgArray, cmap="gray")
    # np.set_printoptions(**defaultPrint_opts)