import serial
import time

PORT = "/dev/ttyTHS1"
BAUD = 9600

with serial.Serial(PORT, BAUD, timeout=1) as ser:
    time.sleep(2)
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    good = 0
    bad = 0

    for i in range(20):
        ser.write(b"PING\n")
        ser.flush()

        reply = ser.readline()
        text = reply.decode("utf-8", errors="replace").strip()

        if text == "PONG":
            good += 1
            print(i, "OK:", text)
        else:
            bad += 1
            print(i, "BAD raw:", repr(reply), "hex:", reply.hex(), "text:", text)

        time.sleep(0.3)

    print("Good:", good, "Bad:", bad)