import numpy as np
import density as density

test_altitudes = [
    0,            # Sea Level
    5000,         # Mid-Troposphere
    11000,        # Tropopause (Boundary 1)
    15000,        # Mid-Stratosphere
    20000         # Stratopause (Boundary 2)
]

# Expected Density (kg/m^3)
# Values are from standard tables, rounded to 4 decimal places
expected_densities = [
    1.2250,       # 0 m
    0.7364,       # 5000 m
    0.3639,       # 11000 m
    0.1948,       # 15000 m
    0.0880        # 20000 m (approximation used in the code)
]

def run_density_test():
    """Runs tests against known ISA values."""
    print("--- Running ISA Density Model Test ---")
    
    # Check if the number of test cases matches
    if len(test_altitudes) != len(expected_densities):
        print("Error: Test case list length mismatch.")
        return

    # Epsilon for float comparison (a small tolerance for numerical errors)
    tolerance = 1e-3  
    
    all_passed = True
    
    for y_test, expected_rho in zip(test_altitudes, expected_densities):
        calculated_rho = density.calculate_density(y_test)
        
        # Check if the calculated value is close to the expected value
        if np.isclose(calculated_rho, expected_rho, atol=tolerance):
            status = "PASS"
        else:
            status = "FAIL"
            all_passed = False
        
        print(f"Altitude: {y_test:<7} m | Calculated ρ: {calculated_rho:.4f} | Expected ρ: {expected_rho:.4f} | Status: {status}")

    print("--------------------------------------")
    if all_passed:
        print("✅ ALL TESTS PASSED! The atmospheric model is correctly implemented.")
    else:
        print("❌ ONE OR MORE TESTS FAILED. Check the calculation in the relevant altitude range.")

# Execute the test script
if __name__ == "__main__":
    run_density_test()