import serial
import time

PORT = "COM5"       # ✅ YOUR PORT
BAUD_RATE = 9600


def read_sensor_data():
    try:
        with serial.Serial(PORT, BAUD_RATE, timeout=2) as ser:
            time.sleep(2)  # Arduino reset delay

            # flush old junk data
            ser.reset_input_buffer()

            while True:
                raw = ser.readline().decode("utf-8", errors="ignore").strip()

                if not raw or raw == "ERR":
                    continue

                try:
                    temp_str, moist_str = raw.split(",")
                    temp = float(temp_str)
                    moisture = int(moist_str)

                    return temp, moisture

                except:
                    continue

    except serial.SerialException:
        return None, None