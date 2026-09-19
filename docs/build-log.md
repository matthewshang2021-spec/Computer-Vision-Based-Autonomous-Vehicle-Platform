# Build Log

## Vision and Steering Milestone

### Completed
- IMX219 camera capture verified
- black lane segmented from background
- lane centroid calculated
- error calculated as `line_center - image_center`
- Jetson/Pico UART verified at 115200 baud
- steering command generated from proportional control
- Pico successfully received `STEER` commands
- S20 servo automatically turned the front wheels

### Example behavior
- error near 0 -> `STEER 0`
- positive error -> positive steering
- negative error -> negative steering

### Next Step
Connect the two MG513X rear motors through the D157B and implement low-speed propulsion with `STOP` and a communication watchdog.

---

## Template

### Date

### Goal

### Hardware Changes

### Software Changes

### Test

### Result

### Problems

### Fix / Next Step
