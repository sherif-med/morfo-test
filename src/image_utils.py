
# Generate 5 batches of 20 randomly generated RGB images of shape (256,512,3).
import numpy as np
from dataclasses import dataclass

def generate_batch_images(batch_size=5, width=256, height=512, bands = 3):
    return np.random.rand(batch_size, width , height, bands)

@dataclass
class Square:
    x: int
    y: int
    size: int

    def is_overlapping(self, other):
        return not (self.x + self.size <= other.x or other.x + other.size <= self.x or self.y + self.size <= other.y or other.y + other.size <= self.y)

def generate_random_squares(
    img_width=256,
    img_height=256,
    square_size=50,
    num_squares=3,
    )-> list[Square]:

    all_squares = []

    attempts = 0
    max_attempts = 1000
    while len(all_squares) < num_squares and attempts < max_attempts:
        x = np.random.randint(0, img_height - square_size)
        y = np.random.randint(0, img_width - square_size)
        s = Square(x, y, square_size)
        if not any([s.is_overlapping(other) for other in all_squares]):
            all_squares.append(s)
        attempts += 1
    if attempts == max_attempts:
        print(f"Warning: Only placed {len(all_squares)}/{num_squares} squares.")

    return all_squares

def burn_squares(img: np.ndarray, squares: list[Square]) -> np.ndarray:
    """
    Turn all pixels in the first square in white and all pixels in the second
    square in black.
    """
    assert len(squares) == 2, "Number of squares must be 2"
    img[squares[0].y:squares[0].y + squares[0].size, squares[0].x:squares[0].x + squares[0].size] = 1
    img[squares[1].y:squares[1].y + squares[1].size, squares[1].x:squares[1].x + squares[1].size] = 0
    return img

def random_image_crop(img: np.ndarray, square_size: int) -> np.ndarray:
    x_start = np.random.randint(0, img.shape[1] - square_size)
    y_start = np.random.randint(0, img.shape[0] - square_size)
    return img[y_start:y_start + square_size, x_start:x_start + square_size]

def random_batch_crop(bacth: np.ndarray, square_size: int) -> np.ndarray:
    # stack cropped images
    return np.stack([random_image_crop(bacth[image_idx], square_size) for image_idx in range(bacth.shape[0])])
