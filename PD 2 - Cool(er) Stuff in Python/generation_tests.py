from image_generator import *
import unittest
import numpy as np
import matplotlib.pyplot as plt
from secrets import randbits

# Make a UnitTest class called generation_tests.

# Write the following tests and make sure your generators pass the tests (because they work).
# Use assertions.
# test_diagonal: creates a diagonal image generator, generates a random image, and makes sure it is diagonally symmetric
# test_gradient: create a gradient image generator, generate a random image, calculate the angle used to generate the image from the seed (you can use your own method here),
#                sample 50 random points from the image, calculate their position along the gradient, make sure the values are close

class generation_tests(unittest.TestCase):
    """     diagonal tests      """
    def test_init_diagonal_and_base_class(self):
        #basic tests
        instParams = {"instName": "dpg", "size": 50}
        paramNames = list(instParams.keys()) 
        DPG = Diagonal_Pattern_Generator(image_size=instParams["size"],
                                          name=instParams["instName"])
        # testing names and dimensions of DPG (derived class)
        self.assertEqual(DPG.name, instParams["instName"], 
                         f"{paramNames[0]} should be {instParams["instName"]}")
        self.assertEqual(DPG.image_size, instParams["size"], 
                         f"{paramNames[1]} should be {instParams["size"]}")
        # testing Image_Generator's (base/super class) generate_image method
        seed = randbits(128)
        img = super(Diagonal_Pattern_Generator, DPG).generate_image(seed=seed)
        computeMean = np.mean(img) 
        computeStd = np.std(img)
        # default decimal places is 7, choose only 1 because of variability from each test execution
        """image array values can be negative?"""
        # self.assertTrue(np.min(img) == 0.0, msg=f"expected min == {0.0}, get {np.min(img)}")
        # self.assertTrue(np.max(img) == 1.0, msg=f"expected max == {1.0}, get {np.max(img)}")

        self.assertAlmostEqual(computeMean, 0.5, places=1, 
                               msg=f"expect mean(img) == 0.5, get {computeMean}")
        self.assertAlmostEqual(computeStd, np.sqrt(0.1), places=1, 
                               msg=f"expected std(img) == sqrt(0.1) get {computeStd}")

    def test_diagonal_pattern_image(self):
        im_size = 50
        DPG = Diagonal_Pattern_Generator(im_size, "DPG_Obj")
        image = DPG.generate_image(seed=randbits(128))
        for i in range(im_size):
            for j in range(im_size):
                self.assertEqual(image[i][j], image[j][i], msg=f"image[{i}][{j}] != image[{j}][{i}]")
        # save image as grayscale to local dir for view
        plt.imsave("diagonal.png", image, cmap="gray")
    
    """     gradient tests     """
    def test_gradient_generate_image(self):
        # class instantiation tests
        gradGen_obj = Gradient_Generator(image_size=50, name = "gradGen_obj")
        self.assertEqual(gradGen_obj.image_size, 50, msg=f"expected 50, got {gradGen_obj.image_size}")
        self.assertEqual(gradGen_obj.name, "gradGen_obj", msg=f"expected name \"gradGen_obj\", \
                         got {gradGen_obj.name}")
        # generate_image tests
        seed = randbits(128)
        image = gradGen_obj.generate_image(seed=seed)
        self.assertEqual(image.shape, (gradGen_obj.image_size, gradGen_obj.image_size),
                         msg=f"expected (50,50), got {image.shape} when seed = {seed}")

        direction = seed % 8
        print("direction = {}".format(direction))
        if direction == 0:
            # left -> right
            # (from left to right, ) first test if the colors are fading
            self.assertTrue(image[:,0] == np.zeros((image.shape[0], 1)), 
                            msg=f"expect the first column to be all 0's when seed = {seed}, \
                            direction = {dir}")
            for col in range(1, image.shape[1]):
                prev = col - 1
                # first check if all columns have same value in each entry
                prev_value, col_value = image[0, prev], image[0, col]
                self.assertEqual(image[:, prev] / prev_value, np.ones((image.shape[0], 1)),
                                 msg=f"assertion failed when seed = {seed}, direction  {dir}, at column {col}")
                self.assertEqual(image[:, col] / col_value, np.ones((image.shape[0], 1)),
                                 msg=f"assertion failed when seed = {seed}, direction  {dir}, at column {col}")
                # then check if the prev entries are smaller than col entries by 1
                self.assertEqual(image[:, col] - image[:, prev], np.ones((image.shape[0], 1)),
                                 msg=f"assertion failed when seed = {seed}, direction  {dir}, at column {col}")
        elif direction == 1:
            # right -> left
            # from right to left, first test if the colors are fading
            self.assertTrue(image[:,image.shape[1] - 1] == np.zeros((image.shape[0], 1)), 
                            msg=f"expect the last column to be all 0's")
            for col in range(image.shape[1] - 1, -1, step=-1):
                prev = col - 1
                # first check if all columns have same value in each entry
                prev_value, col_value = image[0, prev], image[0, col]
                self.assertEqual(image[:, prev] / prev_value, np.ones((image.shape[0], 1)))
                self.assertEqual(image[:, col] / col_value, np.ones((image.shape[0], 1)))
                # then check if the col entries are smaller than prev entries by 1
                self.assertEqual(image[:, prev] - image[:, col], np.ones((image.shape[0], 1)))
        elif direction == 2:
            # top -> bottom
            pass
        elif direction == 3:
            # bottom -> top
            pass
        elif direction == 4:
            pass
        elif direction == 5:
            pass
        elif direction == 6:
            pass
        else:
            pass
        # save image as grayscale to local dir for view
        plt.imsave("gradient.png", image, cmap="gray")

        # Save gradient to another file for debugging and better view 
        np.savetxt("gradient.txt", image, fmt="%.2f", delimiter=', ')