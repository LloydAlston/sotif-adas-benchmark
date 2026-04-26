# Scenario 05 — Sensor Degradation Stress Test (Novel Scenario)  

## SOTIF Trigger  
Gradual sensor performance degradation — fog density increases, camera noise rises  

## Setup  
Baseline AEB scenario executed repeatedly while environmental degradation increases incrementally (0% → 100% fog density).

## Test Conditions  
| Condition Level | Weather        | Visibility |
|----------------|---------------|------------|
| Level 0        | Clear         | 100%       |
| Level 1–3      | Light fog     | 70–90%     |
| Level 4–6      | Moderate fog  | 40–70%     |
| Level 7–10     | Dense fog     | < 40%      |

## Pass/Fail Criterion  
System must avoid collision up to defined minimum visibility threshold; failure boundary must be identified  

## SOTIF Classification  
Performance limitation: progressive degradation of sensor perception under adverse environmental conditions  

## KPIs Measured  
- Detection range vs. degradation level (m)  
- TTC at intervention vs. degradation level  
- Braking performance (m)  
- Sensor confidence score (%)  
- Failure threshold (visibility % at first collision)  
- Collision rate (%) across degradation levels  