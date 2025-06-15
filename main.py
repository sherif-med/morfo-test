from src.image_utils import (
    generate_batch_images,
    generate_random_squares,
    burn_squares,
    random_batch_crop)

from src.stats_utils import stats_to_parquet


def test_pipeline():
    # *Consts def
    batch_size = 20
    image_width = 512
    image_height = 256
    image_bands = 3
    batch_count = 5
    # Generate initial batch
    images_batches = [generate_batch_images(batch_size, image_width, image_height, image_bands) for i in range(batch_count)]
    ## Apply burn_squares
    square_size = 50
    square_count = 2
    for c_batch in range(batch_count):
        for c_image in range(batch_size):
            img = images_batches[c_batch][c_image]
            squares = generate_random_squares(image_width, image_height, square_size, square_count)
            burn_squares(img, squares)
    # Apply random crop
    crop_size = 200
    cropped_batches = [random_batch_crop(batch, crop_size) for batch in images_batches]
    # Calculate stats and save
    stats_to_parquet(cropped_batches, 'test.parquet')

if __name__ == "__main__":
    test_pipeline()
