import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sdlp_calculator import calculate_sdlp

print("=== DRY DAY ===")
sdlp = calculate_sdlp('data/results/s02_ego.csv')
print(f"SDLP: {sdlp:.4f}m")

print("=== DAWN ===")
sdlp_dawn = calculate_sdlp('data/results/s02_ego_dawn.csv')
print(f"SDLP: {sdlp_dawn:.4f}m")

print("=== NIGHT ===")
sdlp_night = calculate_sdlp('data/results/s02_ego_night.csv')
print(f"SDLP: {sdlp_night:.4f}m")