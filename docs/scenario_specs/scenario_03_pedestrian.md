# Scenario 03 — Pedestrian AEB: Jaywalking  

## SOTIF Trigger  
Occlusion — pedestrian enters field of view late  

## Setup  
Pedestrian crosses from behind a parked car at ~5 km/h. Ego vehicle traveling at 30 km/h.

## Test Conditions  
| Condition   | Weather        | Lighting |
|------------|---------------|----------|
| Clear day  | Clear         | Day      |
| Foggy road | Fog (50 m vis)| Day      |
| Night      | Clear         | Night    |

## Pass/Fail Criterion  
Ego vehicle comes to a full stop before entering the pedestrian’s crossing path  

## SOTIF Classification  
Performance limitation: late detection due to occlusion and limited sensor field of view  

## KPIs Measured  
- Time-to-collision (TTC) at detection  
- TTC at intervention  
- Stopping distance (m)  
- Detection latency (ms)  
- Collision rate (%)  