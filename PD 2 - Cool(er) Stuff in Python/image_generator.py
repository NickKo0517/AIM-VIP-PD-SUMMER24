import numpy as np
from numpy.core.multiarray import array as array

# In this class, image values are grayscale from 0.0 to 1.0 (black to white).

class Image_Generator:
    '''
    Image_Generator is a basic class that generates images.
    '''
    def __init__(self, image_size: int, name: str):
        self.image_size = image_size
        self.name = name
        # TODO: other initialization as needed

    def generate_image(self, seed: int) -> np.array:
        """might have to restrict values to range [0.0, 1.0]"""
        # Returns an image_size x image_size array filled with numbers sampled from a Normal distribution with mean 0.5 and variance 0.1.
        # Hint: use numpy.
        # TODO: Write this code.
        rng = np.random.default_rng(seed=seed)
        rawNormal = rng.normal(loc=0.5, scale=np.sqrt(0.1), size=(self.image_size, self.image_size))
        # return np.clip(rawNormal, a_min=0.0, a_max=1.0)     #might be faulty
        return rawNormal

class Diagonal_Pattern_Generator(Image_Generator):
    '''
    Diagonal_Pattern_Generator is a class that generates cool diagonally symmetric patterns.
    '''
    # TODO: Write an __init__ method that initializes the superclass object.
    def __init__(self, image_size: int, name: str):
        super().__init__(image_size=image_size, name=name)

    # TODO: Also write a generate_image method that takes in a numerical seed and 
    # generates an image that's symmetric across the diagonals and is NOT a solid color.
    # TODO: Make the design randomly vary with the seed.
    # Your choice of what the design is. Spend as little or as much time as you want.
    # Hint: if you're lazy, what are some of the cheapest ways you can take an existing image and make it diagonally symmetric?
    def generate_image(self, seed: int) -> np.array:
        image = np.zeros((self.image_size, self.image_size))
        randNumGenerator = np.random.default_rng(seed=seed)
        n_randnums = self.image_size    # number of random numbers in a diagonal 
        # Generate random numbers diagonally starting from the largest diagonal
        for r in range(self.image_size):
            r_cpy = r
            diagonal = randNumGenerator.normal(loc=0.5, scale=np.sqrt(0.1), size=n_randnums)
            # Diagonal fill in
            # (0,0) -> (1,1) -> ... (image_size - 1, image_size - 1)
            # (1, 0) -> (2, 1) -> ... (image_size - 1, image_size -2)
            for c in range(n_randnums):
                image[r][c] = diagonal[c]
                if n_randnums != self.image_size:
                    image[c][r] = image[r][c]
                r += 1
            r = r_cpy
            n_randnums -= 1
        return image 

class Gradient_Generator(Image_Generator):
    '''
    Gradient_Generator is a class that generates black to white gradients in random directions.
    '''
    # TODO: Write an __init__ method that initializes the superclass object.
    def __init__(self, image_size: int, name: str):
        super().__init__(image_size=image_size, name=name)

    # TODO: Also write a generate_image method that generates a gradient from black to white in a specified angle.
    # TODO: Make the angle randomly vary with the seed.
    # TODO: Also draw a line on the image in all gray (0.5) that is parallel to the gradient and passing through the middle of the image.
    def generate_image(self, seed: int) -> np.array:
        img = np.zeros((self.image_size, self.image_size))  
        print(f"dim(img) = {img.shape} at beginning of {self.generate_image.__name__}")
        grad_direction = seed % 8
        grad_pattern = np.linspace(0, self.image_size, self.image_size)

        mid = int(self.image_size / 2) 
        if grad_direction == 0:
            # left to right
            img = np.tile(grad_pattern, (self.image_size, 1))
            img[mid] = 0.5 * np.ones(self.image_size)
        elif grad_direction == 1:
            # right to left
            grad_pattern = np.linspace(self.image_size, 0, self.image_size)
            img = np.tile(grad_pattern, (self.image_size, 1))
            img[mid] = 0.5 * np.ones(self.image_size)
        elif grad_direction == 2:
            # top to bottom
            img = (np.tile(grad_pattern, (self.image_size, 1))).T
            img[:, mid] =  0.5 * np.ones(self.image_size)
        elif grad_direction == 3:
            # bottom to top
            grad_pattern = np.linspace(self.image_size, 0, self.image_size)
            img = (np.tile(grad_pattern, (self.image_size, 1))).T
            img[:, mid] =  0.5 * np.ones(self.image_size)
        elif grad_direction == 4:
            # left upper -> right lower
            pass
        elif grad_direction == 5:
            # right upper -> left lower
            pass
        elif grad_direction == 6:
            # left lower -> right upper
            pass
        else:
            # right lower -> left upper
            pass
        print(f"dim(img) = {img.shape} at end of {self.generate_image.__name__}")
        return img
