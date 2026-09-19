import serial
import time

PORT = "/dev/ttyTHS1"
BAUD = 115200

with serial.Serial(PORT, BAUD, timeout=1) as ser:
    time.sleep(2)
    ser.reset_input_buffer()

    for i in range(20):
        ser.write(b"PING\n")
        reply = ser.readline().decode(errors="replace").strip()
        print(i, reply)
        time.sleep(0.2)