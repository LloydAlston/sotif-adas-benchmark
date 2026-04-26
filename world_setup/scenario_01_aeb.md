# Scenario 01 — AEB: Car-to-Car Rear

## SOTIF Trigger
Sensor detection delay at high relative speed

## Setup
Ego vehicle following lead vehicle. Lead vehicle brakes suddenly at 50 km/h.

## Test Conditions
| Condition | Weather     | Lighting |
|-----------|-------------|----------|
|  Dry day  | Clear       | Day      |
|  Wet night| Rain        | Night    |
| Heavy Rain| Heavy Rain  | Day      |

## Pass/Fail Criterion
TTC > 0.8s at intervention, no collision

## SOTIF Classification
Performance limitation: sensor latency under high closure rate

## KPIs Measured
- TTC at intervention
- Braking distance
- Response latency (ms)
- Collision rate (%)