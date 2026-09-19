import serial
import time

PORT = "/dev/ttyTHS1"
BAUD = 115200

commands = [
    "PING",
    "STEER 0",
    "STEER 15",
    "STEER -15",
    "STEER 30",
    "STEER -30",
    "STEER 0",
    "STOP",
]

with serial.Serial(PORT, BAUD, timeout=2) as ser:
    time.sleep(2)
    ser.reset_input_buffer()

    for cmd in commands:
        print("Jetson sending:", cmd)
        ser.write((cmd + "\n").encode("utf-8"))
        ser.flush()

        reply = ser.readline().decode("utf-8", errors="replace").strip()
        print("Pico replied:", reply if reply else "[no reply]")
        print()

        time.sleep(1)