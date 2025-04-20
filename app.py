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
A = st.slider("Component A (%)", 0, 100, step=5, value=30)
B = st.slider("Component B (%)", 0, 100 - A, step=5, value=30)
C = 100 - A - B

def ternary_to_cartesian(a, b, c):
    total = a + b + c
    # A at top, B at bottom left, C at bottom right
    x = 0.5 * (2 * c + a) / total
    y = (np.sqrt(3) / 2) * a / total
    return x, y

# Vertices for the main triangle
A_vertex = (0.5, np.sqrt(3)/2)
B_vertex = (0, 0)
C_vertex = (1, 0)

# Phase regions: All coordinates are within the triangle
phase_regions = {
    "α": [B_vertex, (0.25, np.sqrt(3)/4), (0.5, 0), (0.25, 0)],
    "β": [(0.25, np.sqrt(3)/4), (0.5, 0), (0.75, np.sqrt(3)/4), (0.5, np.sqrt(3)/2)],
    "γ": [(0.5, 0), C_vertex, (0.75, np.sqrt(3)/4)]
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

    # Main triangle (A at top, B at bottom left, C at bottom right)
    triangle_coords = np.array([B_vertex, C_vertex, A_vertex])
    triangle_patch = patches.Polygon(triangle_coords, closed=True, facecolor="white", edgecolor='black', lw=2)
    ax.add_patch(triangle_patch)

    # Phase regions, clipped to the triangle
    for phase, coords in phase_regions.items():
        phase_patch = patches.Polygon(coords, closed=True, facecolor=phase_colors[phase], edgecolor='black', lw=2, alpha=0.4)
        phase_patch.set_clip_path(triangle_patch)
        ax.add_patch(phase_patch)

    # Draw triangle boundary again for clarity
    ax.plot(*zip(*(triangle_coords.tolist() + [triangle_coords[0].tolist()])), color='black', lw=2)

    # Grid system with tiered styling
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
        # A-axis (bottom, left to right)
        ax.plot([f/2, 1 - f/2], [f*np.sqrt(3)/2]*2, color=color, lw=lw, ls='-')
        # B-axis (right, up to top)
        ax.plot([f, (1 + f)/2], [0, (1 - f)*np.sqrt(3)/2], color=color, lw=lw, ls='-')
        # C-axis (left, up to top)
        ax.plot([(1 - f)/2, 1 - f], [(1 - f)*np.sqrt(3)/2, 0], color=color, lw=lw, ls='-')

        # Add labels
        ax.text(f, -0.04, f"{100 - i}", ha='center', va='top', 
                fontsize=fontsize, fontweight=fontweight, color=color)  # C-axis
        ax.text((1 + f)/2 + 0.03, (1 - f)*np.sqrt(3)/2, f"{100 - i}", ha='left', 
                fontsize=fontsize, fontweight=fontweight, color=color)  # A-axis
        ax.text((1 - f)/2 - 0.03, (1 - f)*np.sqrt(3)/2, f"{100 - i}", ha='right', 
                fontsize=fontsize, fontweight=fontweight, color=color)  # B-axis

    # User point
    ax.plot(x, y, 'ro', markersize=8)
    ax.text(x, y + 0.035, f"({A}, {B}, {C})", ha='center', fontsize=10, fontweight='bold', color='black')

    # Vertex labels
    ax.text(0.5, np.sqrt(3)/2 + 0.05, "A (100%)", ha='center', fontsize=13, fontweight='bold', color='orange')
    ax.text(-0.05, -0.05, "B (100%)", ha='right', fontsize=13, fontweight='bold', color='blue')
    ax.text(1.05, -0.05, "C (100%)", ha='left', fontsize=13, fontweight='bold', color='green')

    # Add legend for phase colors
    legend_patches = [
        patches.Patch(color=phase_colors["α"], label="Phase α (light blue)"),
        patches.Patch(color=phase_colors["β"], label="Phase β (light green)"),
        patches.Patch(color=phase_colors["γ"], label="Phase γ (light coral)")
    ]
    ax.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=3, frameon=True)

    # Set aspect ratio and limits for perfect equilateral triangle
    ax.set_aspect('equal', adjustable='datalim')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, np.sqrt(3)/2)
    ax.axis('off')
    st.pyplot(fig)
