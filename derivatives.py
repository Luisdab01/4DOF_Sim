import numpy as np
import density as density

def derivatives(state, m, cd0, cla, cl0, k, A, I_y, c_bar, C_M0, C_Malpha, C_Mq, C_Mde, thrust, delta_e):
    g = 9.80665

    # --- 1. Access State Variables (6 elements) ---

    u = state[2]
    v = state[3]
    theta = state[4]
    q = state[5] # NEW: Pitch rate is now read from the state vector!

    # Initialize derivative array (must be size 6 now)
    new_derivatives = np.zeros(6)

    # --- 2. Calculate Kinematic Derivatives (x_dot, y_dot, theta_dot) ---
    new_derivatives[0] = u
    new_derivatives[1] = v
    new_derivatives[4] = q

    # --- 3. Calculate Velocities, Angles, and Density (Used for Forces & Moments) ---
    y = state[1]
    rho = density.calculate_density(y)
    V = np.sqrt(u**2 + v**2)
    gamma  = np.arctan2(v,u)
    alpha = theta - gamma

# --- 4. Calculate Forces (L, D) for Linear Acceleration (F_x, F_y) ---
    # ... (Calculate F_x_total and F_y_total)

    grav_acc = np.array([0,-g])
    accel_drag = np.zeros(2)
    accel_lift = np.zeros(2)
    accel_thrust = np.zeros(2)

    # Handle the case of zero velocity to prevent division by zero
    if V > 1e-6:  # Check if speed is not negligible
        cl = cl0 + cla*alpha
        lift_force_mag = 0.5 * rho * V**2 * cl *A

        cd = cd0 + k*cl**2
        drag_force_mag = 0.5 * rho * V**2 * cd * A

        thrust_force_mag = thrust
        

        lift_decel_mag = lift_force_mag / m       
        drag_decel_mag = drag_force_mag / m

        
        thrust_accel_mag = thrust_force_mag / m
        
        # Calculate the unit vector in the direction of velocity
        unit_vector = np.array([u, v]) / V
        perpendicular_unit_vector = np.array([-v,u]) / V
        if perpendicular_unit_vector[1] < 0:
            perpendicular_unit_vector *= -1
        
        # Drag acceleration acts opposite to motion
        accel_drag = -drag_decel_mag * unit_vector
        accel_lift = lift_decel_mag * perpendicular_unit_vector
        accel_thrust[0] = thrust_accel_mag * np.cos(theta)
        accel_thrust[1] = thrust_accel_mag * np.sin(theta)
    
    # Total acceleration is the sum of all accelerations
    total_accel = grav_acc + accel_drag + accel_lift + accel_thrust

    # --- 5. Arrange Linear Accelerations (u_dot, v_dot) ---
    new_derivatives[2] = total_accel[0] #u_dot
    new_derivatives[3] = total_accel[1] #v_dot

    # --- 6. Calculate PITCHING MOMENT (M) for Angular Acceleration (q_dot) ---
    
    # Calculate dimensional pitch rate term for damping
    q_term = q * c_bar / (2 * V) if V > 1e-6 else 0.0

    # Calculate Moment Coefficient (C_M)
    C_M = (C_M0 + 
           C_Malpha * alpha + 
           C_Mq * q_term + 
           C_Mde * delta_e) # NEW FORMULA
           
    # Calculate Net Pitching Moment (M)
    M = 0.5 * rho * V**2 * c_bar * A * C_M
    
    # Calculate Angular Acceleration (q_dot)
    new_derivatives[5] = M / I_y # q_dot = M / I_y (NEW)

    return new_derivatives