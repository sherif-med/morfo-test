
import numpy as np
import pandas as pd
import boto3

def calculate_stats_for_color(batch, color, key_prefix=''):
    """
    """
    color_count = []
    for img in batch:
        is_color = np.all(img == color, axis=-1)
        color_count.append(np.sum(is_color))

    stats = {
        key_prefix+'avg': np.mean(color_count),
        key_prefix+'std': np.std(color_count),
        key_prefix+'min': np.min(color_count),
        key_prefix+'max': np.max(color_count),
    }

    return stats

def calculate_stats(batch):
    """
    """
    white_color = np.array([1, 1, 1])
    black_color = np.array([0, 0, 0])

    stats = calculate_stats_for_color(batch, white_color, 'white_')
    stats.update(calculate_stats_for_color(batch, black_color, 'black_'))

    return stats


def stats_to_parquet(batch_array, output_path) -> pd.DataFrame:
    """
    """
    rows = []
    for batch_id, batch in enumerate(batch_array):
        stats = calculate_stats(batch)
        stats['batch_id'] = batch_id
        rows.append(stats)

    df = pd.DataFrame(rows)
    df = df[['batch_id',
             'white_avg', 'white_min', 'white_max', 'white_std',
             'black_avg', 'black_min', 'black_max', 'black_std']]

    df.to_parquet(output_path, index=False)
    print("Stats saved to {}".format(output_path))

    return df

def stats_to_parquet_and_upload(batch_array, local_path: str, bucket_name: str, key: str):
    """
    """
    # Generate Parquet file locally
    _ = stats_to_parquet(batch_array, local_path)

    # Upload to S3
    s3 = boto3.client('s3')
    with open(local_path, 'rb') as f:
        s3.upload_fileobj(f, bucket_name, key)
    print(f"Uploaded to s3://{bucket_name}/{key}")
