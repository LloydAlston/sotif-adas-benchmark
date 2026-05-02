import pandas as pd
import numpy as np


def calculate_sdlp(csv_path):
    """
    Calculate Standard Deviation of Lateral Position (SDLP)
    
    Args:
        csv_path (str): Path to CSV file containing vehicle_y data
        
    Returns:
        float: SDLP value
    """

    # read CSV
    df = pd.read_csv(csv_path)

    # validate required column exists
    if 'vehicle_y' not in df.columns:
        raise ValueError("CSV must contain 'vehicle_y' column")

    # extract lateral position
    y = df['vehicle_y'].values

    # compute SDLP (sample standard deviation)
    sdlp = np.std(y, ddof=1)

    return sdlp