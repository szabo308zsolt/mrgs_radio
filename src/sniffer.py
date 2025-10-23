#!/usr/bin/env python3
"""
Sniffer using pyrf24-style API.
Scans channels 0..125 and prints any packets it receives (hex).
Adjust CE_PIN and CSN for your wiring.
"""
import time
import sys

# Typical import — many pyrf24 packages expose an RF24-like class.
from pyrf24 import RF24

CE_PIN = 22   # GPIO pin number connected to CE
CSN_BUS = 0   # SPI bus/CS (often 0 for SPI0 CE0)

def main():
    radio = RF24(CE_PIN, CSN_BUS)   # (ce, csn) or (ce, spi_bus, spi_dev) depending on package
    if not radio.begin():
        print("Radio failed to begin. Check wiring and permissions (run as root).")
        sys.exit(1)

    # Basic radio settings
    radio.setAutoAck(False)
    radio.setDataRate(RF24.RATE_1MBPS)
    radio.setPALevel(RF24.PA_LOW)
    radio.setRetries(0, 0)  # disable automatic retransmit
    radio.startListening()

    print("Scanning 2.4 GHz channels (0..125). Press Ctrl-C to stop.")
    try:
        while True:
            for ch in range(0, 126):
                radio.setChannel(ch)
                # short dwell on the channel to catch packets
                start = time.time()
                seen = False
                while time.time() - start < 0.20:
                    if radio.available():
                        seen = True
                        # read all payloads currently available
                        while radio.available():
                            length = radio.getDynamicPayloadSize() if hasattr(radio, "getDynamicPayloadSize") else radio.get_payload_size()
                            payload = radio.read(length) if hasattr(radio, "read") else radio.read_payload(length)
                            # payload may be bytes or bytearray
                            if isinstance(payload, (bytes, bytearray)):
                                print(f"[ch {ch:03d}] {payload.hex()}")
                            else:
                                # some bindings return list of ints
                                try:
                                    b = bytes(payload)
                                    print(f"[ch {ch:03d}] {b.hex()}")
                                except Exception:
                                    print(f"[ch {ch:03d}] {payload}")
                if seen:
                    print(f"Activity detected on channel {ch}")
            # small pause between full sweeps
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nStopping scan.")
    finally:
        radio.end()
        print("Radio closed.")

if __name__ == "__main__":
    main()

