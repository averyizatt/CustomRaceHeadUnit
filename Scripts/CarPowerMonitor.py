#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import subprocess

# Pin config (BCM numbering)
ACC_PIN = 23       # Input: monitors ACC via pin 30 on relay
RELAY_PIN = 24     # Output: controls 5V signal or delay relay

# Delay in seconds before shutdown (e.g. 1 minute for testing)
SHUTDOWN_DELAY = 60

# Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ACC_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RELAY_PIN, GPIO.OUT)

print("Car power monitor running...")

try:
    shutdown_timer = None
    acc_was_on = False

    while True:
        acc_state = GPIO.input(ACC_PIN)

        if acc_state == GPIO.LOW:
            # ACC ON
            if not acc_was_on:
                print("ACC ON detected.")
                acc_was_on = True
                GPIO.output(RELAY_PIN, GPIO.LOW)  # Keep Pi powered
                shutdown_timer = None
        else:
            # ACC OFF
            if acc_was_on:
                print("ACC OFF detected. Starting shutdown timer.")
                acc_was_on = False
                shutdown_timer = time.time()

        if shutdown_timer and (time.time() - shutdown_timer > SHUTDOWN_DELAY):
            print("Shutdown delay elapsed. Shutting down...")
            GPIO.output(RELAY_PIN, GPIO.HIGH)  # Cut relay to power off Pi
            subprocess.run(["sudo", "shutdown", "-h", "now"])

        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting cleanly.")
finally:
    GPIO.cleanup()
