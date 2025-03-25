

pip install matplotlib



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
                [np.sqrt(3) / 2 * fraction, np.sqrt(3) / 2 * fraction], 
                color=color, linestyle='dotted', linewidth=linewidth, alpha=alpha)
        
        # Lines from bottom-left to top (for Component B)
        ax.plot([fraction, 0.5 + fraction / 2], 
                [0, np.sqrt(3) / 2 * (1 - fraction)], 
                color=color, linestyle='dotted', linewidth=linewidth, alpha=alpha)
        
        # Lines from bottom-right to top (for Component C)
        ax.plot([1 - fraction, 0.5 - fraction / 2], 
                [0, np.sqrt(3) / 2 * (1 - fraction)], 
                color=color, linestyle='dotted', linewidth=linewidth, alpha=alpha)
    
    # Add numbers to the grid lines (multiples of 5 and 10) on horizontal lines only
    for i in range(1, num_lines):
        fraction = i / num_lines
        percentage = int(fraction * 100)
        
        if percentage % 5 == 0:
            # Determine text properties based on whether it's a multiple of 10 or 5
            fontsize = 10 if percentage % 10 == 0 else 8
            fontweight = 'bold' if percentage % 10 == 0 else 'normal'
            
            # Annotate horizontal lines (Component A)
            ax.text(0.5 * fraction - 0.02, np.sqrt(3) / 2 * fraction, f"{100-percentage}%", 
                    ha='right', va='center', fontsize=fontsize, 
                    color='black', fontweight=fontweight)
    
    # Labels for the components
    ax.text(0.5, np.sqrt(3) / 2 + 0.05, f"Component A ({A*100:.2f}%)", ha='center', fontsize=12, fontweight='bold', color='darkblue')
    ax.text(1.05, -0.05, f"Component B ({B*100:.2f}%)", ha='right', fontsize=12, fontweight='bold', color='darkgreen')
    ax.text(-0.05, -0.05, f"Component C ({C*100:.2f}%)", ha='left', fontsize=12, fontweight='bold', color='darkred')
    
    # Plot the composition point with a glowing effect
    ax.scatter(x, y, color='gold', s=200, label="Given Composition", edgecolor='black', linewidth=2)
    ax.scatter(x, y, color='gold', s=400, alpha=0.2)  # Glow effect
    
    ax.axis('off')
    
    return fig

# Streamlit app
st.title("Gibbs Triangle Plotter")
A = st.number_input("Enter fraction of Component A", min_value=0.0, max_value=1.0, value=0.0)
B = st.number_input("Enter fraction of Component B", min_value=0.0, max_value=1.0, value=0.0)

if st.button("Plot"):
    if A + B > 1:
        st.error("Composition fractions must sum to 1.")
    else:
        fig = plot_gibbs_triangle(A, B)
        st.pyplot(fig)
