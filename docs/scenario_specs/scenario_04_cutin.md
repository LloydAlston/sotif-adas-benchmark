# Scenario 04 — Cut-In from Blind Spot  

## SOTIF Trigger  
Vehicle entering from outside camera/radar coverage area  

## Setup  
Target vehicle in adjacent lane performs an aggressive cut-in maneuver at highway speed (~120 km/h). Ego vehicle maintains constant velocity.

## Test Conditions  
| Condition | Weather | Lighting |
|----------|--------|----------|
| Clear    | Clear  | Day      |
| Rain     | Rain   | Day      |
| Dusk     | Clear  | Low light|

## Pass/Fail Criterion  
Lateral deviation < 0.3 m and no collision  

## SOTIF Classification  
Performance limitation: incomplete environmental perception due to sensor coverage gaps  

## KPIs Measured  
- Time-to-collision (TTC) at cut-in  
- Minimum lateral distance (m)  
- Lateral deviation (m)  
- System response latency (ms)  
- Collision / near-miss rate (%)  
