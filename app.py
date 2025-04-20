import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
from matplotlib.path import Path

st.title("Ternary Diagram with Random Phase Boundaries")

A = st.slider("Component A (%)", 0, 100, step=5, value=50)
B = st.slider("Component B (%)", 0, 100 - A, step=5, value=30)
C = 100 - A - B

def ternary_to_cartesian(a, b, c):
    total = a + b + c
    x = 0.5 * (2 * c + a) / total
    y = (np.sqrt(3) / 2) * a / total
    return x, y

A_vertex = (0.5, np.sqrt(3)/2)
B_vertex = (0, 0)
C_vertex = (1, 0)

# Define 3 arbitrary regions that together fill the triangle
region1 = [B_vertex, (0.2, 0.2), (0.4, 0.1), (0.5, 0.25), (0.3, 0.4), (0.5, 0.5), A_vertex, B_vertex]
region2 = [(0.4, 0.1), (0.7, 0.1), (0.8, 0.3), (0.7, 0.5), (0.5, 0.5), (0.3, 0.4), (0.5, 0.25), (0.4, 0.1)]
region3 = [C_vertex, (0.7, 0.1), (0.8, 0.3), (0.7, 0.5), A_vertex, (0.5, 0.5), (0.7, 0.5), C_vertex]

phase_regions = {
    "α": region1,
    "β": region2,
    "γ": region3
}

phase_colors = {
    "α": "#b3c6ff",    # light blue
    "β": "#b3ffb3",    # light green
    "γ": "#ffb3b3"     # light coral
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

    triangle_coords = np.array([B_vertex, C_vertex, A_vertex])
    triangle_patch = patches.Polygon(triangle_coords, closed=True, facecolor="white", edgecolor='black', lw=2)
    ax.add_patch(triangle_patch)

    # Draw phase regions, clipped to triangle
    for phase, coords in phase_regions.items():
        phase_patch = patches.Polygon(coords, closed=True, facecolor=phase_colors[phase], edgecolor='black', lw=2, alpha=0.6)
        phase_patch.set_clip_path(triangle_patch)
        ax.add_patch(phase_patch)

    # Draw triangle boundary again for clarity
    ax.plot(*zip(*(triangle_coords.tolist() + [triangle_coords[0].tolist()])), color='black', lw=2)

    # User point
    ax.plot(x, y, 'ro', markersize=10)
    ax.text(x, y + 0.035, f"({A}, {B}, {C})", ha='center', fontsize=11, fontweight='bold', color='black')

    # Vertex labels
    ax.text(0.5, np.sqrt(3)/2 + 0.05, "A (100%)", ha='center', fontsize=13, fontweight='bold', color='orange')
    ax.text(-0.05, -0.05, "B (100%)", ha='right', fontsize=13, fontweight='bold', color='blue')
    ax.text(1.05, -0.05, "C (100%)", ha='left', fontsize=13, fontweight='bold', color='green')

    # Add legend for phase colors
    legend_patches = [
        patches.Patch(color=phase_colors["α"], label="Phase α (blue)"),
        patches.Patch(color=phase_colors["β"], label="Phase β (green)"),
        patches.Patch(color=phase_colors["γ"], label="Phase γ (coral)")
    ]
    ax.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=3, frameon=True)

    ax.set_aspect('equal', adjustable='datalim')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, np.sqrt(3)/2)
    ax.axis('off')
    st.pyplot(fig)
