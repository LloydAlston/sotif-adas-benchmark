import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ttc_calculator import calculate_ttc
from braking_distance import calculate_braking_distance
from sdlp_calculator import calculate_sdlp
from visualisation.plot_ttc import plot_ttc


# Dry day
print("=== DRY DAY ===")
ttc_df = calculate_ttc('data/results/s01_ego_dry.csv', 'data/results/s01_lead_dry.csv')
print(f"Min TTC: {ttc_df['ttc'].min():.2f}s")

braking = calculate_braking_distance('data/results/s01_ego_dry.csv')
print(f"Braking distance: {braking:.2f}m")

print("=== WET NIGHT ===")
ttc_df_wet = calculate_ttc('data/results/s01_ego_wet.csv', 'data/results/s01_lead_wet.csv')
print(f"Min TTC: {ttc_df_wet['ttc'].min():.2f}s")
braking_wet = calculate_braking_distance('data/results/s01_ego_wet.csv')
print(f"Braking distance: {braking_wet:.2f}m")

print("=== HEAVY RAIN ===")
ttc_df_rain = calculate_ttc('data/results/s01_ego_rain.csv', 'data/results/s01_lead_rain.csv')
print(f"Min TTC: {ttc_df_rain['ttc'].min():.2f}s")
braking_rain = calculate_braking_distance('data/results/s01_ego_rain.csv')
print(f"Braking distance: {braking_rain:.2f}m")
# Generate TTC plots for all 3 conditions
conditions = ['dry', 'wet', 'rain']
labels = ['Dry Day', 'Wet Night', 'Heavy Rain']

for condition, label in zip(conditions, labels):
    ttc_df = calculate_ttc(
        f'data/results/s01_ego_{condition}.csv',
        f'data/results/s01_lead_{condition}.csv'
    )
    ttc_df.to_csv(f'data/results/s01_ttc_{condition}.csv', index=False)
    plot_ttc(
        f'data/results/s01_ttc_{condition}.csv',
        'Scenario 1 - AEB',
        label,
        f'data/results/s01_ttc_{condition}.png'
    )
    print(f"Plot saved: s01_ttc_{condition}.png")