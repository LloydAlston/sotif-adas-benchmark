# Scenario 02 — LDW: Lane Departure on Low-Contrast Markings  

## SOTIF Trigger  
Lane marking ambiguity in low contrast (wet road, faded markings)

## Setup  
Ego vehicle traveling on a curved motorway segment. No steering input applied; vehicle gradually drifts toward lane boundary.

## Test Conditions  
| Condition   | Weather | Lighting       |
|------------|--------|----------------|
| Clear day  | Dry    | Day            |
| Low sun    | Clear  | Dawn (glare)   |
| Night drive| Dry/Wet| Night          |

## Pass/Fail Criterion  
LDW alert triggered > 0.5 s before lane marking is crossed

## SOTIF Classification  
Performance limitation: reduced perception accuracy due to low-contrast or ambiguous lane markings

## KPIs Measured  
- Time-to-line-crossing (TLC) at alert  
- Lateral offset at alert (m)  
- Detection confidence of lane markings (%)  
- Warning latency (ms)  
- Missed warning rate (%)  