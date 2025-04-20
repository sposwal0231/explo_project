import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def plot_gibbs_triangle(A, B):
    C = 1 - A - B  # Safe due to prior validation
    
    # Convert to ternary coordinates
    x = 0.5 * (2 * B + A)
    y = (np.sqrt(3) / 2) * A
    
    # Define triangle vertices
    triangle = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3) / 2], [0, 0]])
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Plot the triangle
    ax.plot(triangle[:, 0], triangle[:, 1], 'k-', linewidth=3)
    
    # Plot grid lines
    num_lines = 20
    for i in range(1, num_lines):
        fraction = i / num_lines
        percentage = int(fraction * 100)
        
        # Styling based on percentage
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
        
        # Horizontal lines (Component A)
        ax.plot([0.5 * fraction, 1 - 0.5 * fraction], 
                [np.sqrt(3)/2 * fraction, np.sqrt(3)/2 * fraction], 
                color=color, linestyle='dotted', linewidth=linewidth, alpha=alpha)
        
        # Lines for Component B
        ax.plot([fraction, 0.5 + fraction/2], 
                [0, np.sqrt(3)/2 * (1 - fraction)], 
                color=color, linestyle='dotted', linewidth=linewidth, alpha=alpha)
        
        # Lines for Component C
        ax.plot([1 - fraction, 0.5 - fraction/2], 
                [0, np.sqrt(3)/2 * (1 - fraction)], 
                color=color, linestyle='dotted', linewidth=linewidth, alpha=alpha)
        
        # Annotations
        if percentage % 5 == 0:
            fs = 10 if percentage % 10 == 0 else 8
            fw = 'bold' if percentage % 10 == 0 else 'normal'
            
            # Component A annotations (left edge)
            ax.text(0.5 * fraction - 0.02, np.sqrt(3)/2 * fraction, 
                    f"{100-percentage}%", ha='right', va='center', 
                    fontsize=fs, fontweight=fw, color='black')
            
            # Component B annotations (bottom and right edge)
            ax.text(fraction, -0.02, f"{percentage}%", 
                    ha='center', va='top', fontsize=fs, fontweight=fw, color='black')
            # Right edge (BA) annotations for B
            x_ba = 0.5 + fraction/2
            y_ba = (np.sqrt(3)/2) * (1 - fraction)
            ax.text(x_ba, y_ba, f"{percentage}%", ha='center', va='bottom',
                    rotation=-60, fontsize=fs, fontweight=fw, color='black')
            
            # Component C annotations (bottom and left edge)
            ax.text(1 - fraction, -0.02, f"{percentage}%", 
                    ha='center', va='top', fontsize=fs, fontweight=fw, color='black')
            # Left edge (AC) annotations for C
            x_ac = 0.5 - fraction/2
            y_ac = (np.sqrt(3)/2) * (1 - fraction)
            ax.text(x_ac, y_ac, f"{percentage}%", ha='center', va='bottom',
                    rotation=60, fontsize=fs, fontweight=fw, color='black')
    
    # Vertex labels
    ax.text(0.5, np.sqrt(3)/2 + 0.05, f"Component A ({A*100:.2f}%)", 
            ha='center', fontsize=12, fontweight='bold', color='darkblue')
    ax.text(1.05, -0.05, f"Component B ({B*100:.2f}%)", 
            ha='right', fontsize=12, fontweight='bold', color='darkgreen')
    ax.text(-0.05, -0.05, f"Component C ({C*100:.2f}%)", 
            ha='left', fontsize=12, fontweight='bold', color='darkred')
    
    # Plot composition point
    ax.scatter(x, y, color='gold', s=200, edgecolor='black', linewidth=2)
    ax.scatter(x, y, color='gold', s=400, alpha=0.2)
    
    ax.axis('off')
    return fig

# Streamlit interface
st.title("Gibbs Triangle Plotter")
A = st.number_input("Enter fraction of Component A", min_value=0.0, max_value=1.0, value=0.3)
B = st.number_input("Enter fraction of Component B", min_value=0.0, max_value=1.0, value=0.3)

if st.button("Plot"):
    if (A + B) > 1.0 + 1e-9:
        st.error("A + B cannot exceed 1.0")
    else:
        fig = plot_gibbs_triangle(A, B)
        st.pyplot(fig)
