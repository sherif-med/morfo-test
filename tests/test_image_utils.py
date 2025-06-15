import unittest
import numpy as np
from src.image_utils import (
    generate_batch_images,
    random_batch_crop,
    generate_random_squares,
    burn_squares,
    random_image_crop,
)

class TestImageUtils(unittest.TestCase):
    def test_generate_batch_images(self):
        batch_size = 10
        image_width = 256
        image_height = 256
        image_bands = 3
        batch = generate_batch_images(batch_size, image_width, image_height, image_bands)
        self.assertEqual(batch.shape, (batch_size, image_height, image_width, image_bands))

    def test_random_batch_crop(self):
        batch_size = 10
        image_width = 256
        image_height = 256
        image_bands = 3
        batch = generate_batch_images(batch_size, image_width, image_height, image_bands)
        crop_size = 128
        cropped_batch = random_batch_crop(batch, crop_size)
        self.assertEqual(cropped_batch.shape, (batch_size, crop_size, crop_size, image_bands))

    def test_random_batch_crop_incomplete_data(self):
        batch_size = 10
        image_width = 256
        image_height = 256
        image_bands = 3
        batch = generate_batch_images(batch_size, image_width, image_height, image_bands)
        # Simulate incomplete data by removing some pixels
        batch = batch[:, :, :10, :]
        crop_size = 128
        with self.assertRaises(AssertionError):
            random_batch_crop(batch, crop_size)

    def test_generate_random_squares(self):
        img_width = 256
        img_height = 256
        square_size = 50
        num_squares = 3
        squares = generate_random_squares(img_width, img_height, square_size, num_squares)
        self.assertEqual(len(squares), num_squares)

    def test_burn_squares(self):
        img_width = 256
        img_height = 256
        square_size = 50
        num_squares = 2
        img = np.zeros((img_height, img_width, 3), dtype=np.uint8)
        squares = generate_random_squares(img_width, img_height, square_size, num_squares)
        burned_img = burn_squares(img, squares)
        self.assertEqual(burned_img.shape, (img_height, img_width, 3))

    def test_random_image_crop(self):
        img_width = 256
        img_height = 256
        img_bands = 3
        img = np.random.rand(img_height, img_width, img_bands)
        crop_size = 128
        cropped_img = random_image_crop(img, crop_size)
        self.assertEqual(cropped_img.shape, (crop_size, crop_size, img_bands))

if __name__ == "__main__":
    unittest.main()