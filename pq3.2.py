import math
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')  # Set the backend to non-interactive
from scipy.integrate import quad
import numpy as np

def midpointRule(f, a, b, n):
    """Implements the midpoint rule for numerical integration"""
    step = (b - a) / n
    total = 0
    for i in range(n):
        midpoint = a + (i + 0.5) * step
        total += f(midpoint)
    return step * total

def trapeziumRule(f, a, b, n):
    """Implements the trapezium rule for numerical integration"""
    step = (b - a) / n
    total = 0.5 * (f(a) + f(b))  # Half weights for endpoints
    for i in range(1, n):
        x = a + i * step
        total += f(x)
    return step * total

def simpsonsRule(f, a, b, n):
    """
    Implements Simpson's rule for numerical integration
    Note: n must be even
    """
    if n % 2 != 0:
        raise ValueError("n must be even for Simpson's rule")
    
    step = (b - a) / n
    total = f(a) + f(b)  # Endpoints
    
    # Even-indexed points (multiplier 2)
    for i in range(2, n, 2):
        x = a + i * step
        total += 2 * f(x)
    
    # Odd-indexed points (multiplier 4)
    for i in range(1, n, 2):
        x = a + i * step
        total += 4 * f(x)
    
    return (step / 3) * total

def x32(x):
    return math.pow(x, 1.5)

if __name__ == "__main__":
    true_value, _ = quad(x32, 0, 1)

    # Arrays to store errors
    powers = range(1, 25)
    n_values = [2**i for i in powers]
    midpoint_errors = []
    trapezium_errors = []
    simpson_errors = []

    for n in n_values:
        midpoint_error = abs(midpointRule(x32, 0, 1, n) - true_value)
        trapezium_error = abs(trapeziumRule(x32, 0, 1, n) - true_value)
        simpson_error = abs(simpsonsRule(x32, 0, 1, n) - true_value)
        
        midpoint_errors.append(midpoint_error)
        trapezium_errors.append(trapezium_error)
        simpson_errors.append(simpson_error)

    # Create the plot with dark background grid
    plt.figure(figsize=(12, 8))
    
    # Add custom grid for powers of 2
    plt.grid(True, which="both", ls="-", alpha=0.1)  # Faint regular grid
    
    # Plot vertical lines for powers of 2 first (so they're in the background)
    for i, n in enumerate(n_values):
        plt.axvline(x=n, color='purple', linestyle='-', alpha=0.2, linewidth=1.5)
    
    # Plot the main lines
    plt.loglog(n_values, midpoint_errors, 'o-', label='Midpoint Rule', alpha=0.7)
    plt.loglog(n_values, trapezium_errors, 's-', label='Trapezium Rule', alpha=0.7)
    plt.loglog(n_values, simpson_errors, '^-', label='Simpson\'s Rule', alpha=0.7)

    # Add labels
    plt.xlabel('Number of intervals (n)')
    plt.ylabel('Absolute Error')
    plt.title('Convergence of Numerical Integration Methods')

    # Add reference lines
    max_error = max(max(midpoint_errors), max(trapezium_errors), max(simpson_errors))
    min_n = min(n_values)
    reference_x = np.array([min_n, max(n_values)])

    for order, style in zip([1, 2, 4], ['--', ':', '-.']):
        reference_y = max_error * (reference_x/min_n)**(-order)
        plt.loglog(reference_x, reference_y, style, color='gray', alpha=0.5, 
                label=f'O(n^{order})')

    # Add power annotations with enhanced visibility
    for i, n in enumerate(n_values):
        # Create a small colored box for the text background
        plt.text(n, plt.ylim()[0], f'2^{i+1}', 
                rotation=45, 
                verticalalignment='top', 
                horizontalalignment='right',
                fontsize=9,
                color='purple',
                fontweight='bold',
                bbox=dict(facecolor='white', 
                         edgecolor='purple',
                         alpha=0.8,
                         pad=2))
        
        # Highlight points with larger markers
        plt.plot(n, midpoint_errors[i], 'o', markersize=8)
        plt.plot(n, trapezium_errors[i], 's', markersize=8)
        plt.plot(n, simpson_errors[i], '^', markersize=8)

    plt.legend()
    plt.tight_layout()
    plt.savefig('integration_error3.png', bbox_inches='tight', dpi=300)