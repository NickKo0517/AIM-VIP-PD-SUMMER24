from image_generator import *
import unittest
import numpy as np
from secrets import randbits

# Make a UnitTest class called generation_tests.

# Write the following tests and make sure your generators pass the tests (because they work).
# Use assertions.
# test_diagonal: creates a diagonal image generator, generates a random image, and makes sure it is diagonally symmetric
# test_gradient: create a gradient image generator, generate a random image, calculate the angle used to generate the image from the seed (you can use your own method here),
#                sample 50 random points from the image, calculate their position along the gradient, make sure the values are close

class generation_tests(unittest.TestCase):
    """Required test suite that contains test_diagonal and test_gradient""" 
    def test_diagonal(self):
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

        # default decimal places is 7, choose only 1 and 2 because of variability
        self.assertAlmostEqual(computeMean, 0.5, places=1, 
                               msg=f"expect mean(img) == 0.5, get {computeMean}")
        self.assertAlmostEqual(computeStd, np.sqrt(0.1), places=2, 
                               msg=f"expected std(img) == sqrt(0.1) get {computeStd}")