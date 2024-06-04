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
    def test_init_diagonal(self):
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
        # testing if the superclass image_generator's generate_image method
        seed = randbits(128)
        img = super(Diagonal_Pattern_Generator, DPG).generate_image(seed=seed)
        computeMean = np.mean(img) 
        computeStd = np.std(img)
        # default decimal places is 7, choose only 1 because of variability from each test execution
        self.assertTrue(np.min(img) == 0.0, msg=f"expected min == {0.0}, get {np.min(img)}")
        self.assertTrue(np.max(img) == 1.0, msg=f"expected max == {1.0}, get {np.max(img)}")
        self.assertAlmostEqual(computeMean, 0.5, places=1, 
                               msg=f"expect mean(img) == 0.5, get {computeMean}")
        self.assertAlmostEqual(computeStd, np.sqrt(0.1), places=1, 
                               msg=f"expected std(img) == sqrt(0.1) get {computeStd}")
        
        def test_generate_image(self):
            image = Image_Generator(image_size=50, name="testImg")