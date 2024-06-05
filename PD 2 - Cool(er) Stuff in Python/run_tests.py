from generation_tests import *
import matplotlib.pyplot as plt

if __name__ == "__main__":
    unittest.main()

    """     view image generated    """
    # size, name = 50, "testing"
    # image = Diagonal_Pattern_Generator(image_size=size, name=name)
    # # image = Diagonal_Pattern_Generator(image_size=size, name=name)
    # imgArray = image.generate_image(seed=randbits(128))
    # for elem in imgArray:
    #     assert not isinstance(elem, type(None)), f"elem at {np.where(imgArray == elem)}"
    # plt.imsave("test_img.png", imgArray, cmap="gray")
    
    # """ Save imgArray to another file for debugging and better view """
    # np.savetxt("imgMatrix.txt", imgArray ,fmt="%.2f", delimiter=', ')