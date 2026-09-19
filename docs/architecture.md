# Architecture

```text
IMX219 camera
      |
      v
Jetson Nano
  - capture frame
  - detect black lane
  - calculate lane center/error
  - calculate steering command
      |
      | UART 115200
      v
Raspberry Pi Pico 2
  - steering PWM
  - rear-motor PWM/direction
  - safety watchdog
      |
      +--> S20 steering servo
      |
      +--> D157B dual motor driver
              |        |
              v        v
          MG513X-L  MG513X-R
```

Steering convention:
```text
negative STEER -> left
STEER 0        -> straight
positive STEER -> right
```

Vision error:
```text
error = line_center_x - image_center_x
```

October scope intentionally excludes IMU fusion, ToF sensing, GPS, SLAM, and WRO-specific drivetrain changes.
