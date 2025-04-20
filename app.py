import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
from matplotlib.path import Path

# Title and description
st.title("Ternary Diagram with Phase Regions")
st.markdown("""
Adjust components **A** and **B**. Component **C** is calculated automatically.  
Your selected composition will be placed on the triangle and the corresponding **phase region** will be shown.
""")

# Component sliders
C = st.slider("Component C (%)", 0, 100, step=5, value=30)
A = st.slider("Component A (%)", 0, 100 - C, step=5, value=30)
B = 100 - A - C

def ternary_to_cartesian(a, b, c):
    total = a + b + c
    x = 0.5 * (2 * b + c) / total
    y = (np.sqrt(3) / 2) * c / total
    return x, y

phase_regions = {
    "α": [(0.0, 0.0), (0.4, 0.0), (0.2, 0.3)],
    "β": [(0.4, 0.0), (1.0, 0.0), (0.7, 0.6), (0.2, 0.3)],
    "γ": [(0.2, 0.3), (0.7, 0.6), (0.5, np.sqrt(3)/2)]
}

phase_colors = {
    "α": "lightblue",
    "β": "lightgreen",
    "γ": "lightcoral"
}

def get_phase(x, y):
    for phase, coords in phase_regions.items():
        path = Path(coords)
        if path.contains_point((x, y)):
            return phase
    return "Unknown"

if A + B > 100:
    st.error("Invalid input: A + B exceeds 100%")
else:
    x, y = ternary_to_cartesian(A, B, C)
    phase = get_phase(x, y)
    st.success(f"Composition: A = {A}%, B = {B}%, C = {C}% → Phase: **{phase}**")

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_facecolor("white")

    # Main triangle
    triangle_coords = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]])
    triangle_patch = patches.Polygon(triangle_coords, closed=True, facecolor="white", edgecolor='black', lw=2)
    ax.add_patch(triangle_patch)

    # Phase regions
    for phase, coords in phase_regions.items():
        phase_patch = patches.Polygon(coords, closed=True, facecolor=phase_colors[phase], edgecolor='black', lw=2, alpha=0.5)
        ax.add_patch(phase_patch)

    # Phase boundaries
    boundary_lines = [
        [(0.0, 0.0), (0.4, 0.0), (0.2, 0.3)],
        [(0.4, 0.0), (1.0, 0.0), (0.7, 0.6), (0.2, 0.3)],
        [(0.2, 0.3), (0.7, 0.6), (0.5, np.sqrt(3)/2)]
    ]
    
    for line in boundary_lines:
        ax.plot(*zip(*line), color='black', lw=2)

    # Modified grid system with tiered styling
    for i in range(5, 100, 5):
        f = i / 100
        is_major = i % 10 == 0  # Check for multiples of 10
        
        # Style configuration
        if is_major:
            color = '#404040'  # Dark gray
            lw = 2
            fontsize = 10
            fontweight = 'bold'
        else:
            color = '#808080'  # Medium gray
            lw = 1.5
            fontsize = 8
            fontweight = 'normal'

        # Draw grid lines
        ax.plot([f/2, 1 - f/2], [f*np.sqrt(3)/2]*2, color=color, lw=lw, ls='-')
        ax.plot([f, (1 + f)/2], [0, (1 - f)*np.sqrt(3)/2], color=color, lw=lw, ls='-')
        ax.plot([(1 - f)/2, 1 - f], [(1 - f)*np.sqrt(3)/2, 0], color=color, lw=lw, ls='-')

        # Add labels
        ax.text(f, -0.04, f"{100 - i}", ha='center', va='top', 
                fontsize=fontsize, fontweight=fontweight, color=color)  # B-axis
        ax.text((1 + f)/2 + 0.03, (1 - f)*np.sqrt(3)/2, f"{100 - i}", ha='left', 
                fontsize=fontsize, fontweight=fontweight, color=color)  # C-axis
        ax.text((1 - f)/2 - 0.03, (1 - f)*np.sqrt(3)/2, f"{100 - i}", ha='right', 
                fontsize=fontsize, fontweight=fontweight, color=color)  # A-axis

    # User point
    ax.plot(x, y, 'ro', markersize=8)
    ax.text(x, y + 0.035, f"({A}, {B}, {C})", ha='center', fontsize=10, fontweight='bold', color='black')

    # Vertex labels
    ax.text(-0.05, -0.05, "B (100%)", ha='right', fontsize=11, fontweight='bold', color='blue')
    ax.text(1.05, -0.05, "C (100%)", ha='left', fontsize=11, fontweight='bold', color='green')
    ax.text(0.5, np.sqrt(3)/2 + 0.05, "A (100%)", ha='center', fontsize=11, fontweight='bold', color='orange')

    ax.set_aspect('equal')
    ax.axis('off')
    st.pyplot(fig)
