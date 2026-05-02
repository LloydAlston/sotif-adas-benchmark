import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kpis.ttc_calculator import calculate_ttc
from kpis.braking_distance import calculate_braking_distance
from kpis.sdlp_calculator import calculate_sdlp

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