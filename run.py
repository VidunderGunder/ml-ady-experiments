#%%
import numpy as np
import onnxruntime as rt
import random
import time
from adafruit_servokit import ServoKit
import time

session = rt.InferenceSession("unity.onnx")

inputs = session.get_inputs()
outputs = session.get_outputs()

print("INPUT INFO:")
for i in inputs:
    print(f"{i.name:35}{i.shape}")

print("\nOUTPUT INFO:")
for r in outputs:
    print(f"{r.name:35}{r.shape}")

# Visual placeholder
vp = -1

#%%

def sim(z1, z2, z3):
    return session.run(
        output_names=[
            "continuous_actions",
            "discrete_actions",
        ],
        input_feed={
            "vector_observation": np.array(
                [
                    [
                        0,
                        0,
                        z1,
                        0,
                        0,
                        z2,
                        0,
                        0,
                        z3,
                    ]
                ]
            ).astype(np.float32),
            "visual_observation_0": np.array(
                [
                    [
                        [
                            [vp, vp, vp, vp, vp, vp, vp],
                            [vp, vp, vp, vp, vp, vp, vp],
                            [vp, vp, vp, vp, vp, vp, vp],
                            [vp, vp, vp, vp, vp, vp, vp],
                            [vp, vp, vp, vp, vp, vp, vp],
                            [vp, vp, vp, vp, vp, vp, vp],
                            [vp, vp, vp, vp, vp, vp, vp],
                        ]
                    ]
                ]
            ).astype(np.float32),
            "visual_observation_1": np.array(
                [
                    [
                        [
                            [vp, vp, vp, vp, vp, vp, vp],
                            [vp, vp, vp, vp, vp, vp, vp],
                            [vp, vp, vp, vp, vp, vp, vp],
                            [vp, vp, vp, vp, vp, vp, vp],
                            [vp, vp, vp, vp, vp, vp, vp],
                            [vp, vp, vp, vp, vp, vp, vp],
                            [vp, vp, vp, vp, vp, vp, vp],
                        ]
                    ]
                ]
            ).astype(np.float32),
            "action_masks": np.array(
                [
                    [-1, -1],
                    [-1, -1],
                ]
            ).astype(np.float32),
        },
    )

results = sim(10, 9.9, 9.8)

print("\nONNX RESULTS:")
for r in results:
    print(r)

# %%

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=8)

# %%

# print("Steer")
# kit.servo[0].angle = 180
# time.sleep(1)
# kit.servo[0].angle = 0
# time.sleep(1)
kit.continuous_servo[1].throttle = 1
time.sleep(1)
kit.continuous_servo[1].throttle = -1
time.sleep(1)
kit.continuous_servo[1].throttle = 0

# %%

period_in_seconds = 10
end_time = time.time() + period_in_seconds

loop_counter = 0

while time.time() < end_time:
    z1 = end_time - time.time()
    z2 = z1 - 0.1
    z3 = z2 - 0.1
    
    actions = sim(z1, z2, z3)

    torque = actions[0][0][0]
    steer = actions[0][0][1]

    kit.continuous_servo[1].throttle = torque
    kit.servo[0].angle = 90 + 90 * steer

    loop_counter += 1

print("Loops: " + str(loop_counter))

# %%
