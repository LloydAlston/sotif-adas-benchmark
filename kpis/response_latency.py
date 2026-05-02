import pandas as pd
import numpy as np


def calculate_response_latency(csv_path):
    """
    Response latency = t_intervention - t_trigger

    Trigger: lead vehicle brake > 0
    Intervention: ego vehicle brake > 0
    """

    # read CSV
    df = pd.read_csv(csv_path)

    required_cols = ['timestamp', 'brake_lead', 'brake_ego']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    # find trigger time (lead starts braking)
    trigger_rows = df[df['brake_lead'] > 0]

    if trigger_rows.empty:
        return np.inf  # no trigger event

    t_trigger = trigger_rows.iloc[0]['timestamp']

    # find intervention time (ego starts braking)
    intervention_rows = df[df['brake_ego'] > 0]

    if intervention_rows.empty:
        return np.inf  # no response

    t_intervention = intervention_rows.iloc[0]['timestamp']

    # compute latency
    latency_ms = (t_intervention - t_trigger) * 1000
    return latency_ms