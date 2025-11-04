import numpy as np
import derivatives as der
import matplotlib.pyplot as plt
import threading
from pynput import keyboard
import controls



# --- Initial Conditions ---
m = 1.0
x_0 = 0.0
y_0 = 100.0
u_0 = 20.0
v_0 = 0.0
theta_initial = 0.68
cd0 = 0.025
cl0 = 0.3
cla = 5.5 #per rad
k = 0.06
A = 0.01
dt = 0.01
t_final = 100.0
initial_thrust = 2.44

# --- Initialization ---
flight_control_data = controls.FlightControl(theta_initial, initial_thrust)
keyboard_controller = controls.KeyboardController(flight_control_data)
state = np.array([x_0, y_0, u_0, v_0])
t = 0.0

# Lists to store position data for plotting
x_positions = [x_0]
y_positions = [y_0]

# --- Setup Live Plotting ---
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot(x_positions, y_positions, label='Trajectory')
ax.set_title('2D Aircraft Simulator (W/S for Lift)', fontsize=16)
ax.set_xlabel('Horizontal Distance (m)', fontsize=12)
ax.set_ylabel('Vertical Distance (m)', fontsize=12)
ax.grid(True)
plt.legend()
plt.ion()
plt.show()

# --- Start the Keyboard Listener ---
keyboard_controller.start()

# --- Main Simulation Loop ---
try:
    while state[1] >= 0 and t < t_final:
        with flight_control_data.lock:
            current_theta = flight_control_data.theta
            current_thrust = flight_control_data.thrust

        k1 = der.derivatives(state, m, cd0, cla, cl0, k, A, current_thrust,current_theta)
        k2 = der.derivatives(state + k1 * dt / 2, m, cd0, cla, cl0, k, A, current_thrust, current_theta)
        k3 = der.derivatives(state + k2 * dt / 2, m, cd0, cla, cl0, k, A, current_thrust,current_theta)
        k4 = der.derivatives(state + k3 * dt, m, cd0, cla, cl0, k, A, current_thrust,current_theta)
        
        state = state + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        t += dt

        x_positions.append(state[0])
        y_positions.append(state[1])
        
        line.set_data(x_positions, y_positions)
        ax.set_xlim(min(x_positions), max(x_positions) + 10)
        ax.set_ylim(min(y_positions), max(y_positions) + 10)
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(0.01)

except KeyboardInterrupt:
    print("Simulation stopped by user.")
finally:
    keyboard_controller.stop()
    plt.ioff()
    plt.show()
    print(t)