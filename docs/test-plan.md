# Test Plan

## Stage 1 — Motor Driver Bench Test
Vehicle lifted.

| Test | Expected result |
|---|---|
| Left motor 20% forward | Left wheel spins forward |
| Left motor STOP | Stops |
| Right motor 20% forward | Right wheel spins forward |
| Right motor STOP | Stops |
| Both motors 20% forward | Both spin forward |
| STOP | Both stop |

## Stage 2 — Manual Low-Speed Driving
Success: drives forward, STOP works immediately, steering remains controllable, no resets/overheating.

## Stage 3 — Vision + Fixed Speed
Use camera steering and 15–25% rear-motor PWM.

## Stage 4 — Curves
Tune ROI, Kp, steering limit, and speed.

## Stage 5 — Robustness
Add line-lost STOP, UART watchdog STOP, turn-speed reduction, repeated-run testing.

October target: at least 8 successful runs out of 10 on the same track.
