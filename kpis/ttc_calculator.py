import pandas as pd
import numpy as np


def calculate_ttc(ego_csv, lead_csv):
    # read both CSVs
    ego = pd.read_csv(ego_csv)
    lead = pd.read_csv(lead_csv)

    # align by frame (inner join keeps common frames only)
    df = pd.merge(ego, lead, on='frame', suffixes=('_ego', '_lead'))

    # calculate relative distance (Euclidean distance)
    df['relative_distance'] = np.sqrt(
        (df['vehicle_x_lead'] - df['vehicle_x_ego'])**2 +
        (df['vehicle_y_lead'] - df['vehicle_y_ego'])**2 +
        (df['vehicle_z_lead'] - df['vehicle_z_ego'])**2
    )

    # convert km/h to m/s
    df['v_ego_ms'] = df['velocity_kmh_ego'] / 3.6
    df['v_lead_ms'] = df['velocity_kmh_lead'] / 3.6

    # calculate relative velocity (closing speed)
    df['relative_velocity'] = df['v_ego_ms'] - df['v_lead_ms']

    # calculate TTC
    df['ttc'] = df['relative_distance'] / df['relative_velocity']

    # handle edge cases
    df.loc[df['relative_velocity'] <= 0, 'ttc'] = np.inf  # not closing or moving apart
    df.loc[df['ttc'] < 0, 'ttc'] = np.inf                # invalid negative TTC
    # remove infinite TTC values before returning
    df = df[df['ttc'] != np.inf]
    df = df[df['ttc'] < 30]  # cap at 30 seconds (anything higher is not meaningful)
    return df