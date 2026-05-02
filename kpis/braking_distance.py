import pandas as pd
import numpy as np


def calculate_braking_distance(csv_path):
    # read CSV
    df = pd.read_csv(csv_path)

    # ensure required columns exist
    required_cols = ['brake', 'velocity_kmh', 'vehicle_x', 'vehicle_y']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    # find first frame where brake > 0.5
    braking_start_idx = df[df['brake'] > 0.5].index

    if len(braking_start_idx) == 0:
        return 0.0  # no braking event

    start_idx = braking_start_idx[0]

    # find first frame after that where speed_ms < 0.1
    stop_condition = df.loc[start_idx:]
    stopped_idx = stop_condition[stop_condition['velocity_kmh'] < 0.5].index

    if len(stopped_idx) == 0:
        return np.inf  # never came to a stop

    end_idx = stopped_idx[0]

    # extract positions
    start_pos = df.loc[start_idx, ['vehicle_x', 'vehicle_y']].values
    end_pos = df.loc[end_idx, ['vehicle_x', 'vehicle_y']].values

    # calculate Euclidean distance
    distance = np.linalg.norm(end_pos - start_pos)

    return distance