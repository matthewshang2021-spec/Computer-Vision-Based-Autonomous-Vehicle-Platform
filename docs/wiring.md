# Wiring

## Pico to D157B
| Pico 2 | D157B |
|---|---|
| GP6 | AIN1 |
| GP7 | AIN2 |
| GP8 | BIN1 |
| GP9 | BIN2 |
| GND | GND |

## Steering
Keep the already-tested steering connection:
```text
Pico steering GPIO -> S20 signal
regulated 5V       -> S20 V+
common GND          -> S20 GND
```

## Development Power Split
```text
WHEELTEC 12V battery
        |
        v
5V regulated supply
        |
        +--> Jetson Nano
        +--> Pico 2

Tattu 3S 11.1V battery
        |
        v
D157B
   |        |
   v        v
MG513X-L  MG513X-R
```

If the servo uses actuator-side 5V power, connect Pico GND and actuator GND together.
