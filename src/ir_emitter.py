import RPi.GPIO as GPIO
import time

from ir_simple import ir_sniffer

GPIO.setmode(GPIO.BCM)

IR_PIN = 17
FREQ = 1 / 38000

GPIO.setup(IR_PIN, GPIO.OUT)

LOW = GPIO.LOW
HIGH = GPIO.HIGH

def ir_emitter():
    for i in range(3):
        with open("ir_signals2.csv","r") as file:
            for line in file:
                processed_line = line.strip()
                if processed_line == "1":
                    GPIO.output(IR_PIN, HIGH)
                elif processed_line == "0":
                    GPIO.output(IR_PIN, LOW)
                time.sleep(FREQ)
    GPIO.cleanup()


if __name__ == "__main__":
    ir_emitter()

