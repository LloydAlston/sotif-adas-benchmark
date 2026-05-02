import pandas as pd
import matplotlib.pyplot as plt


def plot_ttc(csv_path, scenario_name, condition, output_path):
    # read CSV
    df = pd.read_csv(csv_path)

    # check required columns
    if 'timestamp' not in df.columns or 'ttc' not in df.columns:
        raise ValueError("CSV must contain 'timestamp' and 'ttc' columns")

    # sort by time (important for correct plotting)
    df = df.sort_values('timestamp')

    # plot
    plt.figure(figsize=(10, 5))
    plt.plot(df['timestamp'], df['ttc'], label='TTC', linewidth=1.5)

    # add safety threshold line
    plt.axhline(y=0.8, color='red', linestyle='--', label='Safety threshold (0.8s)')

    # labels and title
    plt.xlabel('Time (s)')
    plt.ylabel('Time to Collision (TTC) [s]')
    plt.title(f"TTC Analysis - {scenario_name} ({condition})")
    plt.legend()
    plt.grid(True)

    # save plot
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()