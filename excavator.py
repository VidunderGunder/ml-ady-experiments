# %%
import RPi.GPIO as GPIO
import time

# %%
print("Initializing...")

# Pin Definitions
right = 19
left = 26
right_reverse = 6
left_reverse = 13
arm = 5
arm_reverse = 11

pins = [right, left, left_reverse, right_reverse, arm, arm_reverse]

# Pin Setup:
# Board pin-numbering scheme
GPIO.setmode(GPIO.BCM)

for pin in pins:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

# %%
print("Starting now...")
time.sleep(3)
for pin in pins:
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin, GPIO.LOW)

# %%
GPIO.cleanup()
