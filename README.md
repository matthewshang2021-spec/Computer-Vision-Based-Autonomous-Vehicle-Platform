# Computer-Vision-Based Autonomous Vehicle Platform

A camera-based robotics project built on a Wheeltec R3X Ackermann-steering chassis. The current milestone connects black-line detection on a Jetson Nano to front-wheel steering through a Raspberry Pi Pico 2.

The longer-term goal is low-speed line following with rear-motor control and verified stopping behavior when vision or communication fails.

## Current status

The [build log](docs/build-log.md) records successful camera capture, black-line detection, line-center/error calculation, Jetson-to-Pico UART communication, and automatic front-wheel steering with the S20 servo.

The next documented milestone is rear-motor control through the D157B driver, beginning with the drive wheels lifted, followed by low-speed manual driving.

The public repository currently contains Jetson camera, vision, UART, and steering scripts. Pico firmware and an integrated propulsion/line-following program are not yet included. Recorded trial results and demonstration media are also not yet included; the repeated-run target in the test plan is a goal, not a measured result.

## System overview

```text
IMX219 camera
    |
    v
Jetson Nano
  capture image -> detect black line -> calculate horizontal error
  -> calculate proportional steering command
    |
    | UART: 115200 baud in the steering script
    v
Raspberry Pi Pico 2 -> S20 servo -> front-wheel steering

Planned propulsion path:
Pico 2 -> D157B dual-motor driver -> left and right rear motors
```

See [architecture](docs/architecture.md) and [wiring](docs/wiring.md) for the documented design. Rear-motor control and the safety watchdog are design goals whose implementation cannot yet be inspected in the public source.

## Black-line detection and steering

`jetson/line_steer_test.py` implements the current camera-to-steering path:

1. Capture a CSI camera image at a configured output size of 640 x 360 pixels.
2. Select the region between 55% and 95% of the image height.
3. Convert to grayscale, blur, and apply inverse Otsu thresholding.
4. Select the largest contour and accept it if its area exceeds 500 pixels and its centroid can be calculated.
5. Calculate `error = line_center_x - image_center_x` in pixels.
6. Apply a 20-pixel deadband; otherwise calculate `int(0.06 * error)` and clamp the command to -12 through +12.
7. Send a newline-terminated `STEER <value>` command over `/dev/ttyTHS1`.

Negative error means the detected line is left of image center; positive error means it is right. The documented command convention is negative for left and positive for right. The relationship between command values and physical wheel angles still needs calibration documentation.

When no line is detected, this script sends `STEER 0`. This centers steering; it does not issue a motor `STOP` command. The serial request/reply operation blocks, so the configured camera frame rate does not establish the actual control-loop rate.

This approach uses classical image processing and proportional control. A separate Canny/Hough lane-boundary experiment is included in `lane_detection_test.py`.

## Hardware

| Component | Documented role |
|---|---|
| Jetson Nano B01 | Vision and high-level control |
| Raspberry Pi Pico 2 | Steering interface; planned motor control and watchdog |
| DFRobot DFR0924 | Pico terminal breakout |
| IMX219 77-degree camera | Visual line sensing |
| Wheeltec R3X | Ackermann-steering chassis |
| Wheeltec S20 | Steering servo |
| 2 x MG513XP28 12V | Rear drive motors |
| Wheeltec D157B / AT8236 | Planned dual-motor control |
| Tattu 3S 11.1V 1300mAh 45C | Motor/actuator battery |
| Wheeltec 12V 2550mAh battery | Compute-side battery during development |

## Repository guide

| File | Purpose |
|---|---|
| `jetson/test_camera.py` | CSI camera capture/display test |
| `jetson/lane_detection_test.py` | Canny/Hough lane-boundary detection experiment |
| `jetson/line_detect_backup.py` | Black-line contour detection and pixel error display |
| `jetson/line_steer_test.py` | Black-line detection connected to UART steering commands |
| `jetson/test_pico_uart.py` | PING and LED command checks |
| `jetson/uart_stability_test.py` | Repeated PING request/reply checks at 115200 baud |
| `jetson/uart_s2.py` | Separate 9600-baud PING diagnostic with good/bad counts |
| `jetson/s20f_test.py` | Fixed steering-command sequence |
| `jetson/servo_calibrate.py` | Interactive steering commands limited to -15 through +15 |
| `jetson/test_steer_command.py` | Command sequence including steering values up to +/-30 and STOP |
| `pico/README.md` | Target command protocol and safety behavior; firmware not included |
| `docs/architecture.md` | System design and steering convention |
| `docs/wiring.md` | Motor-driver pin assignments and development power split |
| `docs/build-log.md` | Recorded milestone summary and future log template |
| `docs/test-plan.md` | Staged motor, driving, and robustness test plan |

The scripts use different baud rates and command ranges. Match each diagnostic to the installed Pico firmware and verified steering limits before running it. Filenames containing `test` describe manual hardware diagnostics rather than an automated test suite.

## Software environment

The Jetson scripts use Python, OpenCV with GStreamer/CSI-camera support, NumPy, and pyserial, depending on the script. Camera windows require a graphical display.

Exact tested JetPack, Python, library, and Pico firmware versions have not yet been recorded. The repository is not yet a complete reproduction package: the installed Pico firmware, complete UART/servo pin assignments, and confirmed startup instructions are still needed.

## Testing and next milestones

Follow the [staged test plan](docs/test-plan.md):

1. Verify each rear motor and STOP with drive wheels lifted.
2. Verify low-speed manual driving and steering.
3. Integrate vision steering with fixed low-speed propulsion.
4. Evaluate curves while changing one tuning parameter at a time.
5. Verify line-loss stopping, communication timeout, and repeated-run reliability.

Before moving trials, verify motor-off startup and stopping behavior with the installed Pico firmware. For each trial, record the software version, track and lighting conditions, settings, outcome, and failures. The existing target is at least 8 successful runs out of 10 on the same track; success criteria and measured outcomes remain to be documented.

## Bench-test precautions

- Test propulsion with the drive wheels off the ground first and use low PWM initially.
- Keep propulsion disabled during steering-only experiments.
- Verify regulator outputs and battery polarity with a multimeter before connecting power.
- Follow the documented common-ground requirements and verify the actual wiring.
- Verify STOP and communication-timeout behavior before relying on them. Centering steering alone does not stop propulsion.

## License

[MIT License](LICENSE).
