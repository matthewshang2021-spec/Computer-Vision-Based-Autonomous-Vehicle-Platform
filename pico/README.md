# Pico Code

Target command set:
```text
PING
STEER <value>
MOTOR <left> <right>
STOP
```

Safety:
- boot with motors off
- invalid command keeps motors off
- no valid drive command for ~0.5 s -> stop motors
- STOP always overrides drive
