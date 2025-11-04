import numpy as np
import density as density

def derivatives(state, m, cd0, cla, cl0, k, A, thrust,theta):
    g = 9.80665
    u = state[2]
    v = state[3]
    y = state[1]


    new_derivatives = np.zeros(4)
    new_derivatives[0] = u
    new_derivatives[1] = v

    # --- DYNAMIC DENSITY CALCULATION (rho is now calculated here) ---
    rho = density.calculate_density(y)

    
    V = np.sqrt(u**2+v**2)
    grav_acc = np.array([0,-g])
    accel_drag = np.zeros(2)
    accel_lift = np.zeros(2)
    accel_thrust = np.zeros(2)
    
    gamma  = np.arctan2(v,u)
    alpha = theta - gamma
    
    # Handle the case of zero velocity to prevent division by zero
    if V > 1e-6:  # Check if speed is not negligible
        cl = cl0 + cla*alpha
        lift_force_mag = 0.5 * rho * V**2 * cl *A
        lift_decel_mag = lift_force_mag / m

        cd = cd0 + k*cl**2
        drag_force_mag = 0.5 * rho * V**2 * cd * A
        drag_decel_mag = drag_force_mag / m

        thrust_force_mag = thrust
        thrust_accel_mag = thrust_force_mag / m
        
        # Calculate the unit vector in the direction of velocity
        unit_vector = np.array([u, v]) / V
        perpendicular_unit_vector = np.array([-v,u]) / V
        if perpendicular_unit_vector[1] < 0:
            perpendicular_unit_vector *= -1
        
        # Drag acceleration acts opposite to motion
        accel_drag = -drag_decel_mag * unit_vector
        accel_lift = lift_decel_mag * perpendicular_unit_vector
        accel_thrust = thrust_accel_mag * unit_vector
    
    # Total acceleration is the sum of all accelerations
    total_accel = grav_acc + accel_drag + accel_lift + accel_thrust
    
    new_derivatives[2] = total_accel[0]
    new_derivatives[3] = total_accel[1]
    return new_derivatives