import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

IR_PIN = 17
FREQ = 1 / 38000

GPIO.setup(IR_PIN, GPIO.IN)

def ir_sniffer():
    with open("ir_signals2.txt","a") as file:
        file.write("timestanp\n")

        while True:
            state = GPIO.input(IR_PIN)
            read = '1' if state else '0'
            file.write(read + ",\n")
            time.sleep(FREQ)

if __name__ == "__main__":
    ir_sniffer()

