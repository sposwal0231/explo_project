import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def plot_gibbs_triangle(A, B):
    C = 1 - A - B
    
    # Check if composition sums to 1
    if not (abs(A + B + C - 1) < 1e-6):
        raise ValueError("Composition fractions must sum to 1.")
    
    # Convert to ternary coordinates
    x = 0.5 * (2 * B + A)
    y = (np.sqrt(3) / 2) * A
    
    # Define triangle vertices
    triangle = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3) / 2], [0, 0]])
    
    # Create a figure
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Plot the triangle
    ax.plot(triangle[:, 0], triangle[:, 1], 'k-', linewidth=3)
    
    # Plot 20 equidistant grid lines for each component
    num_lines = 20
    for i in range(1, num_lines):
        fraction = i / num_lines
        percentage = int(fraction * 100)
        
        if percentage % 10 == 0:
            color = 'red'
            linewidth = 1.5
            alpha = 0.8
        elif percentage % 5 == 0:
            color = 'blue'
            linewidth = 1
            alpha = 0.6
        else:
            color = 'gray'
            linewidth = 0.5
            alpha = 0.3
        
        # Horizontal lines (parallel to base, for Component A)
        ax.plot([0.5 * fraction, 1 - 0.5 * fraction], 
                [np.sqrt(3) / 2 * fraction, np.sqrt(3) / 2 * fraction)], 
                color=color, linestyle='dotted', linewidth=linewidth, alpha=alpha)
        
        # Lines from bottom-left to top (for Component B)
        ax.plot([fraction, 0.5 + fraction / 2], 
                [0, np.sqrt(3) / 2 * (1 - fraction)], 
                color=color, linestyle='dotted', linewidth=linewidth, alpha=alpha)
        
        # Lines from bottom-right to top (for Component C)
        ax.plot([1 - fraction, 0.5 - fraction / 2], 
                [0, np.sqrt(3) / 2 * (1 - fraction)], 
                color=color, linestyle='dotted', li
