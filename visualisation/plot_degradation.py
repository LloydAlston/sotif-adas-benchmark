import matplotlib.pyplot as plt


def plot_degradation_curve(fog_levels, collision_rates, output_path):
    # plot fog % on x-axis, collision rate on y-axis
    plt.figure(figsize=(10, 5))
    plt.plot(fog_levels, collision_rates, marker='o', label='Collision Rate')

    # find failure boundary (first fog level where collision_rate > 0)
    failure_boundary = None
    for f, c in zip(fog_levels, collision_rates):
        if c > 0:
            failure_boundary = f
            break

    # draw vertical red dashed line at failure boundary
    if failure_boundary is not None:
        plt.axvline(x=failure_boundary, color='red', linestyle='--',
                    label=f'Failure boundary ({failure_boundary}%)')

    # add labels and title
    plt.xlabel('Fog Density (%)')
    plt.ylabel('Collision Rate (%)')
    plt.title('Sensor Degradation Curve: Fog vs Collision Rate')
    plt.grid(True)
    plt.legend()

    # save
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()