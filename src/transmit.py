#!/usr/bin/env python3
"""
Simple transmitter (replay) using pyrf24-style API.
Replace CHANNEL and PAYLOAD_HEX with values you captured from the sniffer.
"""
import time
import sys
from pyrf24 import RF24

CE_PIN = 22
CSN_BUS = 0

# --------- USER CONFIG ----------
CHANNEL = 76                # set to the channel you found
PAYLOAD_HEX = "a1b2c3d4"    # set to the captured payload hex string
WRITE_PIPE = b"\xe7\xe7\xe7\xe7\xe7"   # typical 5-byte address - adjust if needed
INTERVAL = 1.0              # seconds between sends
# --------------------------------

def main():
    radio = RF24(CE_PIN, CSN_BUS)
    if not radio.begin():
        print("Radio begin failed. Check wiring and permissions.")
        sys.exit(1)

    radio.stopListening()
    radio.setDataRate(RF24.RATE_1MBPS)
    radio.setPALevel(RF24.PA_LOW)
    radio.setAutoAck(False)
    radio.setChannel(CHANNEL)
    radio.openWritingPipe(WRITE_PIPE)

    payload = bytes.fromhex(PAYLOAD_HEX)

    print(f"Sending payload {payload.hex()} on channel {CHANNEL} to pipe {WRITE_PIPE.hex()}. Ctrl-C to stop.")
    try:
        while True:
            ok = radio.write(payload)
            if ok:
                print(f"Sent: {payload.hex()}")
            else:
                print("Send failed (no ack, or radio busy).")
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        radio.end()
        print("Radio closed.")

if __name__ == "__main__":
    main()

