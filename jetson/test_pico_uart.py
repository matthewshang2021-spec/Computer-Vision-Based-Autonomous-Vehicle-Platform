import serial
import time

PORT = "/dev/ttyTHS1"
BAUD = 115200

def send(ser, command):
    print("Jetson sending:", command)
    ser.write((command + "\n").encode("utf-8"))
    ser.flush()
    reply = ser.readline().decode("utf-8", errors="replace").strip()
    print("Pico replied:", reply if reply else "[no reply]")
    print()

with serial.Serial(PORT, BAUD, timeout=2) as ser:
    time.sleep(2)
    ser.reset_input_buffer()

    send(ser, "PING")
    time.sleep(1)

    send(ser, "LED ON")
    time.sleep(1)

    send(ser, "LED OFF")