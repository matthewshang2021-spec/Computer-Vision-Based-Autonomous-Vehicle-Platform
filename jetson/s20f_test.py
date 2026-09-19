import serial
import time

PORT = "/dev/ttyTHS1"
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(1)

def send(cmd):
    print("Jetson ->", cmd)
    ser.write((cmd + "\n").encode())
    ser.flush()
    time.sleep(0.1)

    reply = ser.readline().decode(errors="replace").strip()
    print("Pico   ->", reply)

send("PING")
time.sleep(1)

send("STEER 0")
time.sleep(2)

send("STEER -10")
time.sleep(3)

send("STEER 10")
time.sleep(3)

send("STEER 0")
time.sleep(2)

ser.close()