# R3X Vision Autocar

A camera-based autonomous black-line-following car built on a Wheeltec R3X Ackermann-steering chassis.

## October 2026 Goal
Build a reliable car that uses an IMX219 camera on a Jetson Nano to detect a black lane, calculates lane-center error, sends steering commands to a Raspberry Pi Pico 2 over UART, steers the front wheels with the Wheeltec S20 servo, drives the two rear MG513X motors, and stops safely if the lane is lost or communication fails.

## Hardware
| Component | Role |
|---|---|
| Jetson Nano B01 | Vision and high-level control |
| Raspberry Pi Pico 2 | Steering, motor control, safety |
| DFRobot DFR0924 | Pico terminal breakout |
| IMX219 77° camera | Lane sensing |
| Wheeltec R3X | Ackermann chassis |
| Wheeltec S20 | Steering servo |
| 2× MG513XP28 12V | Rear drive motors |
| Wheeltec D157B / AT8236 | October dual-motor driver |
| Tattu 3S 11.1V 1300mAh 45C | Motor/actuator battery |
| Wheeltec 12V 2550mAh battery | Compute-side battery during development |

## Already Completed
- IMX219 camera working
- black-line detection
- line-center calculation
- error calculation
- Jetson → Pico UART
- automatic steering command
- Pico → S20 servo
- automatic front-wheel steering

## Current Development Stage
Next milestone: control the two MG513X rear motors through the D157B, first with the car lifted, then with low-speed manual driving.

## Software
```text
jetson/
  camera_test.py
  line_detect.py
  line_steer.py
  line_follow.py

pico/
  main.py

docs/
  architecture.md
  wiring.md
  build-log.md
  test-plan.md
```

## Safety
Test propulsion with the drive wheels off the ground first. Use low PWM initially. Keep a STOP command and communication timeout in Pico firmware. Verify regulator outputs and battery polarity with a multimeter before connecting power.
