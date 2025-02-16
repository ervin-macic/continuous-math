import numpy as np
import matplotlib.pyplot as plt

def count_representable_numbers(start, end, step):
    """Count how many representable floating point numbers exist in an interval."""
    current = start
    count = 0
    while current < end:
        count += 1
        current += step

    return count

def analyze_float_distribution():
    # Define the ranges we want to analyze (powers of 2)
    ranges = []
    counts = []
    
    # We'll go from 2^0 to 2^7 (1 to 128)
    for i in range(8):
        start = 2**i
        end = 2**(i+1)
        step = 2**(-23 + i)  # Step size increases as we move to higher ranges
        
        count = count_representable_numbers(start, end, step)
        ranges.append(f"{start}-{end}")
        counts.append(count)
    
    # Create the visualization
    plt.figure(figsize=(12, 6))
    
    # Create bar plot
    bars = plt.bar(ranges, counts)
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom')
    
    plt.title('Distribution of Representable 32-bit Floating Point Numbers\nAcross Power-of-2 Intervals')
    plt.xlabel('Intervals')
    plt.ylabel('Number of Representable Values')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Add grid for better readability
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Calculate and print some statistics
    total_numbers = sum(counts)
    print(f"\nTotal representable numbers analyzed: {total_numbers:,}")
    print("\nDetailed breakdown:")
    for i, (range_str, count) in enumerate(zip(ranges, counts)):
        step_size = 2**(-23 + i)
        print(f"Range {range_str}: {count:,} numbers (step size: {step_size})")
    
    # Save the plot instead of displaying it
    plt.savefig('float32_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

# Run the analysis
analyze_float_distribution()