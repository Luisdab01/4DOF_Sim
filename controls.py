import threading
from pynput import keyboard
import numpy as np

# Define constants for control sensitivity
PITCH_RATE_STEP = 0.05  # 0.05 radians/s (approx 2.86 degrees/s)
THRUST_STEP = 0.05

# The Shared Control Object
class FlightControl:
    def __init__(self, initial_delta_e, initial_thrust):
        self.delta_e = initial_delta_e
        self.thrust = initial_thrust
        self.lock = threading.Lock()

# The Keyboard Listener Class
class KeyboardController:
    def __init__(self, control_data):
        self.control_data = control_data
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
    
    def on_press(self, key):
        ELEVATOR_STEP = np.deg2rad(1.0) # 1 degree deflection step (in radians)
        try:
            if key.char == 'w':
                with self.control_data.lock:
                    self.control_data.delta_e += ELEVATOR_STEP 
                    print(f"Elevator up. New delta_e: {np.rad2deg(self.control_data.delta_e):.2f} deg")
            elif key.char == 's':
                with self.control_data.lock:
                    self.control_data.delta_e -= ELEVATOR_STEP
                    print(f"Elevator down. New delta_e: {np.rad2deg(self.control_data.delta_e):.2f} deg")
            elif key.char == 't':
                with self.control_data.lock:
                    self.control_data.thrust += THRUST_STEP
                    print(f"Thrust increased. New Thrust: {self.control_data.thrust:.2f} N")
            elif key.char == 'g':
                with self.control_data.lock:
                    self.control_data.thrust = max(0.0, self.control_data.thrust - THRUST_STEP) # Clamp thrust at zero
                    print(f"Thrust decreased. New Thrust: {self.control_data.thrust:.2f} N")
        except AttributeError:
            pass
    
    def on_release(self, key):
        pass

        # Stop listening with 'Esc'
        if key == keyboard.Key.esc:
            return False

    def start(self):
        self.listener.start()
    
    def stop(self):
        self.listener.stop()