import matplotlib.pyplot as plt


def plot_collision_rate(results_dict, output_path):
    # extract labels and values
    labels = list(results_dict.keys())
    values = list(results_dict.values())

    # create bar chart
    plt.figure(figsize=(12, 6))

    bars = plt.bar(labels, values)

    # colour bars green if 0%, red if > 0%
    for bar, value in zip(bars, values):
        if value == 0:
            bar.set_color('green')
        else:
            bar.set_color('red')

    # add labels and title
    plt.xlabel('Scenario')
    plt.ylabel('Collision Rate (%)')
    plt.title('Collision Rate Across Scenarios')
    plt.xticks(rotation=45, ha='right')

    # optional grid for readability
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    # save to output_path
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()