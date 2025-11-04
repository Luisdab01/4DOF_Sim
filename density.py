import numpy as np

def calculate_density(y):
    # Constants for the International Standard Atmosphere (ISA) Troposphere
    T0 = 288.15      # Sea level temperature (Kelvin)
    rho0 = 1.225     # Sea level density (kg/m^3)
    g = 9.80665      # Gravity (m/s^2)
    L = 0.0065       # Standard temperature lapse rate (K/m)
    R = 287.05287       # Specific gas constant for air (J/kg·K)
    
    y_tropopause = 11000.00  # Altitude limit for the Troposphere (m)
    
    if y <= 0:
        return rho0  # At or below sea level
    elif y < y_tropopause:
        # Troposphere formula: Density decreases with altitude
        T = T0 - L * y
        rho = rho0 * (T / T0)**( (g / (R * L)) - 1 )
        return rho
    else:
        T = 216.65
        exponent = (-g * (y - y_tropopause)) / (R * T)
        P = 22632.06 * np.exp(exponent)
        rho = P / (R*T)
        return rho