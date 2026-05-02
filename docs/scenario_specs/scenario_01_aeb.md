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

## Results

| Condition  | Min Trigger Distance | Verdict |
|------------|---------------------|---------|
| Dry day    | 17m                 | Pass  |
| Wet night  | 17m                 | Pass  |
| Heavy rain | 15m                 | Pass  |

## Key Finding
AEB must trigger at minimum 17m (dry/wet) and 15m (heavy rain) to prevent collision at 50 km/h.
Performance boundary identified between 14–17m depending on weather condition.

## KPI Results

| Condition  | Min TTC | TTC Pass? | Braking Distance |
|------------|---------|-----------|-----------------|
| Dry day    | 1.08s   |  Pass    | 12.39m          |
| Wet night  | 0.53s   |  Fail    | 8.13m           |
| Heavy rain | 0.61s   |  Fail    | 9.59m           |