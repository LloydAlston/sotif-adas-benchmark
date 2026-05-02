import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ttc_calculator import calculate_ttc
from braking_distance import calculate_braking_distance
from sdlp_calculator import calculate_sdlp

# Dry day
print("=== DRY DAY ===")
ttc_df = calculate_ttc('data/results/s01_ego_dry.csv', 'data/results/s01_lead_dry.csv')
print(f"Min TTC: {ttc_df['ttc'].min():.2f}s")

braking = calculate_braking_distance('data/results/s01_ego_dry.csv')
print(f"Braking distance: {braking:.2f}m")