import serial
import time

PORT = "/dev/ttyTHS1"
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(1)

print("S20F steering calibration")
print("Enter angle from -15 to +15")
print("Enter q to quit")
print()

while True:
    value = input("STEER angle: ").strip()

    if value.lower() == "q":
        break

    try:
        angle = float(value)

        # Temporary calibration safety limit
        if angle < -15 or angle > 15:
            print("For now use only -15 to +15")
            continue

        command = "STEER " + str(angle)

        ser.write((command + "\n").encode())
        ser.flush()

        reply = ser.readline().decode(
            errors="replace"
        ).strip()

        print("Pico:", reply)

    except ValueError:
        print("Please enter a number.")

ser.write(b"STEER 0\n")
ser.close()