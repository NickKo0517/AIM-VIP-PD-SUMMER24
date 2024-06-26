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
        # save image as grayscale to local directory for view
        # plt.imsave("diagonal.png", image, cmap="gray")
    
    """     gradient tests     """
    def test_gradient_generate_image(self):
        # class instantiation tests
        gradGen_obj = Gradient_Generator(image_size=50, name = "gradGen_obj")
        self.assertEqual(gradGen_obj.image_size, 50, 
                         msg=f"expected 50, got {gradGen_obj.image_size}")
        self.assertEqual(gradGen_obj.name, "gradGen_obj", 
                         msg=f"expected name \"gradGen_obj\", "
                         f"got {gradGen_obj.name}")
        # generate_image tests
        seed = randbits(128)
        direction = seed % 8
        image = gradGen_obj.generate_image(seed=seed)
        self.assertEqual(image.shape, (gradGen_obj.image_size, gradGen_obj.image_size),
                         msg=f"expected (50,50), got {image.shape}" +
                         f"when seed = {seed}, direction = {direction}")

        # save image as grayscale to local dir for view
        plt.imsave("gradient.png", image, cmap="gray")
        # Save gradient to another file for debugging and better view 
        np.savetxt("gradient.txt", image, fmt="%.2f", delimiter=', ')

        mid = int(image.shape[1] / 2)
        if direction == 0:
            # left -> right
            # (from left to right, ) check fading colors
            self.assertFalse(np.all(image[:mid, 0], axis=0),  # AND all elements: expect all zeros (false)
                            msg=f"expect image[:mid, 0] to be all 0's when seed = {seed}," + 
                            f"direction = {direction}")
            self.assertFalse(np.all(image[mid + 1:, 0], axis=0), # AND all elements: expect all zeros (false)
                            msg= f"expext image[mid+1: 0] to be all 0's when seed = {seed}, " +
                            f"direction = {direction}")

            for col in range(1, image.shape[1]):
                prev = col - 1
                # first check if all columns have same value in each entry
                prev_value, col_value = image[0, prev], image[0, col]
                if prev_value != 0 and col_value != 0:
                    #prev checks
                    self.assertTrue(np.all(image[:mid, prev] / prev_value, axis=0), # AND all elements in column: expect all ones 
                                    msg=f"assertion failed when seed = {seed}, direction = {direction} at column {prev}")
                    self.assertTrue(np.all(image[mid + 1:, prev] / prev_value, axis=0), # AND all elements in column: expect all ones 
                                    msg=f"assertion failed when seed = {seed}, direction  {direction}, at column {prev}")
                    #col checks
                    self.assertTrue(np.all(image[:mid, col] / col_value, axis=0), # AND all elements in column: expect all ones 
                                    msg=f"assertion failed when seed = {seed}, direction = {direction} at column {col}")
                    self.assertTrue(np.all(image[mid + 1:, col] / col_value , axis=0), # AND all elements in column: expect all ones 
                                    msg=f"assertion failed when seed = {seed}, direction = {direction}, at column {col}")

                    # then check if the prev entries are smaller than col entries by 1
                    diff = image[:mid, col] - image[:mid, prev]
                    self.assertTrue(np.all(diff, axis=0), # AND across entire column, expect all ones (true)
                                    msg=f"assertion failed when seed = {seed}, direction =  {direction}," +
                                    f" between column {prev}, {col}")
                    diff = image[mid + 1:, col] - image[mid + 1:, prev]
                    self.assertTrue(np.all(diff, axis=0), # AND across entire column, expect all ones (true)
                                    msg=f"assertion failed when seed = {seed}, direction = {direction}," +
                                    f" between column {prev}, {col}")
        elif direction == 1:
            # right -> left
            # from right to left, check fading colors
            lastColumn = image.shape[1] - 1
            self.assertTrue(not(np.all(image[:mid, lastColumn], axis=0)),   # AND all elements: expect all zeros (false)
                            msg=f"expect image[:mid, lastColumn] to be all 0's when seed = {seed}," + 
                            f"direction = {direction}")
            self.assertTrue(not(np.all(image[mid + 1:, lastColumn], axis=0)), # AND all elements: expect all zeros (false)
                            msg= f"expext image[mid+1:, lastColumn] to be all 0's when seed = {seed}, " +
                            f"direction = {direction}")
            for col in range((image.shape[1] - 1), -1, -1):
                prev = col - 1
                # first check if all columns have same value in each entry
                prev_value, col_value = image[0, prev], image[0, col]
                if prev_value != 0 and col_value != 0:
                    # prev checks
                    self.assertTrue(np.all((image[:mid, prev] / prev_value), axis=0), 
                                    msg=f"not all elements are identical in column {prev}")
                    self.assertTrue(np.all((image[mid + 1:, prev] / prev_value), axis=0), 
                                    msg=f"not all elements are identical in column {prev}")
                    # col checks
                    self.assertTrue(np.all((image[:mid, col] / col_value), axis=0),
                                    msg=f"not all elements are identical in column {col}")
                    self.assertTrue(np.all((image[mid + 1:, col] / col_value), axis=0),
                                    msg=f"not all elements are identical in column {col}")
                    # then check if the col entries are smaller than prev entries by 1
                    self.assertTrue(np.all((image[:mid, prev] - image[:mid, col]), axis=0), 
                                    msg=f"not all values between column {prev} and {col} differ by 1")
                    self.assertTrue(np.all((image[mid + 1:, prev] - image[mid + 1:, col]), axis=0), 
                                    msg=f"not all values between column {prev} and {col} differ by 1")
        elif direction == 2:
            # top -> bottom
            # first check the first ROW: AND across first row, expect all zeros (false)
            self.assertFalse(np.all(image[0, :mid]), 
                             msg=f"image[0, :{mid}] not all zeroes")
            self.assertFalse(np.all(image[0, mid + 1:]), 
                             msg=f"image[0, {mid + 1}:] not all zeroes")
            for row in range(1, image.shape[0]):
                prev = row - 1
                prev_val, row_val = image[prev, 0], image[row, 0]
                if prev_val != 0 and row_val != 0:
                    # prev checks
                    self.assertTrue(np.all(image[prev, :mid] / prev_val),
                                    msg=f"not all elements in image[{prev}, :{mid}] are identical")
                    self.assertTrue(np.all(image[prev, mid + 1:] / prev_val),
                                    msg=f"not all elements in image[{prev}, :{mid}] are identical")
                    # row checks
                    self.assertTrue(np.all(image[row, :mid] / row_val),
                                    msg=f"not all elements in image[{row}, :{mid}] are identical")
                    self.assertTrue(np.all(image[row, mid + 1:] / row_val),
                                    msg=f"not all elements in image[{row}, :{mid}] are identical")
                    # diff = row - prev checks
                    diff = image[row, :mid] - image[prev, :mid]
                    self.assertTrue(np.all(diff), 
                                    msg=f"not all elements in image[{row}, :{mid}] - image[{prev}, :{mid}]" + \
                                        " are identicial")
                    diff = image[row, mid + 1:] - image[prev, mid + 1:]
                    self.assertTrue(np.all(diff), 
                                    msg=f"not all elements in image[{row}, {mid + 1}:] - image[{prev}, {mid + 1}:]" + \
                                        " are identicial")
        elif direction == 3:
            # bottom -> top
            # first check the first ROW: AND across first row, expect all zeros (false)
            self.assertFalse(np.all(image[image.shape[0] - 1, :mid]), 
                             msg=f"image[{image.shape[0] - 1}, :{mid}] not all zeroes")
            self.assertFalse(np.all(image[image.shape[0] - 1, mid + 1:]), 
                             msg=f"image[{image.shape[0] - 1}, {mid + 1}:] not all zeroes")
            for row in range(image.shape[0] - 1, -1, -1):
                prev = row - 1
                prev_val, row_val = image[prev, 0], image[row, 0]
                if prev_val != 0 and row_val != 0:
                    # prev checks
                    self.assertTrue(np.all(image[prev, :mid] / prev_val),
                                    msg=f"not all elements in image[{prev}, :{mid}] are identical")
                    self.assertTrue(np.all(image[prev, mid + 1:] / prev_val),
                                    msg=f"not all elements in image[{prev}, :{mid}] are identical")
                    # row checks
                    self.assertTrue(np.all(image[row, :mid] / row_val),
                                    msg=f"not all elements in image[{row}, :{mid}] are identical")
                    self.assertTrue(np.all(image[row, mid + 1:] / row_val),
                                    msg=f"not all elements in image[{row}, :{mid}] are identical")
                    # diff = prev - row checks
                    diff = image[prev, :mid] - image[row, :mid]
                    self.assertTrue(np.all(diff), 
                                    msg=f"not all elements in image[{prev}, :{mid}] - image[{row}, :{mid}]" + \
                                    " are identicial")
                    diff = image[prev, mid + 1:] - image[row, mid + 1:]
                    self.assertTrue(np.all(diff), 
                                    msg=f"not all elements in image[{prev}, {mid + 1}:] - image[{row}, {mid + 1}:]" + \
                                    " are identicial")
        elif direction == 4:
            pass
        elif direction == 5:
            pass
        elif direction == 6:
            pass
        else:
            pass