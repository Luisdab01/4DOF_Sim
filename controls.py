import threading
from pynput import keyboard

# The Shared Control Object
class FlightControl:
    def __init__(self, initial_theta, initial_thrust):
        self.theta = initial_theta
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
        try:
            if key.char == 'w':
                with self.control_data.lock:
                    self.control_data.theta += 0.05
                    print(f"Pitch angle increased. New theta: {self.control_data.theta:.2f}")
            elif key.char == 's':
                with self.control_data.lock:
                    self.control_data.theta -= 0.05
                    print(f"Pitch angle decreased. New theta: {self.control_data.theta:.2f}")
            if key.char == 't':
                with self.control_data.lock:
                    self.control_data.thrust += 0.05
                    print(f"Thrust increased. New Thrust: {self.control_data.thrust:.2f}")
            elif key.char == 'g':
                with self.control_data.lock:
                    self.control_data.thrust -= 0.05
                    print(f"Thrust decreased. New Thrust: {self.control_data.thrust:.2f}")
        except AttributeError:
            pass
    
    def on_release(self, key):
        if key == keyboard.Key.esc:
            return False

    def start(self):
        self.listener.start()
    
    def stop(self):
        self.listener.stop()