#%%
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
 
"""Simple test for a standard servo on channel 0 and a continuous rotation servo on channel 1."""
import time
from adafruit_servokit import ServoKit
from adafruit_pca9685 import PCA9685
 
#%%
# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
channels = 16
kit = ServoKit(
    channels=channels,
    frequency=360
)

#%%
def wait():
    period = 3
    for second in range(period):
        if period > 2:
            print(str(period - second) + "...")
        time.sleep(1)

#%%
# Throttle test
throttle_channel = 7
print("Positive")
kit.continuous_servo[throttle_channel].throttle = .2
wait()
print("Negative")
kit.continuous_servo[throttle_channel].throttle = -.2
wait()
print("Zero")
kit.continuous_servo[throttle_channel].throttle = 0

#%%
# Steering test

channels = 16
steering_channel = 6

frequencies = [
    50,
    # 100,
    # 200,
    # 250,
    # 275,
    360,
    300,
    400,
    320,
    380,
    340,
    420,
    280,
    # 330,
    # 350,
    # 370,
    # 390,
    # 425,
    # 450,
]

left = 0
right = 120
center = int(right / 2)

for f in frequencies:

    print("Testing frequenzy " + str(f))
    kit = ServoKit(
        channels=channels,
        frequency=f, # Apx. in range 300-400
        address=0x40, # sudo i2cdetect -r -y 1
        i2c=None
    )

    def steer_test(deg):
        print("Steering to " + str(deg))
        kit.servo[steering_channel].angle = deg
        wait()

    kit.servo[steering_channel].set_pulse_width_range(1000, 2000)
    # kit.servo[steering_channel].actuation_range = right

    print("Testing steering")
    # kit.servo[steering_channel].set_pulse_width_range()

    for deg in range(180 + 1):
        if deg % 10 == 0:
            print(deg)
        kit.servo[steering_channel].angle = 0
        time.sleep(0.05)
    print("0 deg")
    # steer_test(center)
    # steer_test(left)
    # steer_test(right)
    


print("Steering test complete")

# %%
