import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
from matplotlib.path import Path

# Title and description
st.title("🌑 Ternary Diagram (Dark Theme) with Phase Regions")
st.markdown("""
Adjust components **A** and **B**. Component **C** is calculated automatically.  
Your selected composition will be placed on the triangle and the corresponding **phase region** will be shown.
""")

# Component sliders
A = st.slider("Component A (%)", 0, 100, step=5, value=30)
B = st.slider("Component B (%)", 0, 100 - A, step=5, value=30)
C = 100 - A - B

# Convert ternary to Cartesian coordinates
def ternary_to_cartesian(a, b, c):
    total = a + b + c
    x = 0.5 * (2 * b + c) / total
    y = (np.sqrt(3) / 2) * c / total
    return x, y

# Define phase regions (in cartesian space)
phase_regions = {
    "α": [(0.0, 0.0), (0.4, 0.0), (0.2, 0.3)],
    "β": [(0.4, 0.0), (1.0, 0.0), (0.7, 0.6), (0.2, 0.3)],
    "γ": [(0.2, 0.3), (0.7, 0.6), (0.5, np.sqrt(3)/2)]
}

# Determine which phase the composition falls into
def get_phase(x, y):
    for phase, coords in phase_regions.items():
        path = Path(coords)
        if path.contains_point((x, y)):
            return phase
    return "Unknown"

# Composition check
if A + B > 100:
    st.error("Invalid input: A + B exceeds 100%")
else:
    x, y = ternary_to_cartesian(A, B, C)
    phase = get_phase(x, y)
    st.success(f"Composition: A = {A}%, B = {B}%, C = {C}% → Phase: **{phase}**")

    # Plot setup
    fig, ax = plt.subplots(figsize=(8, 8))  # Size increased by 1 unit
    ax.set_facecolor("#1e1e1e")  # Dark background

    # Draw main triangle
    triangle_coords = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]])
    triangle_patch = patches.Polygon(triangle_coords, closed=True, facecolor="#2e2e2e", edgecolor='white', lw=2)
    ax.add_patch(triangle_patch)

    # Draw phase regions (clip strictly inside triangle)
    phase_colors = {'α': '#4f81bd', 'β': '#f58f82', 'γ': '#93d19b'}
    for phase, coords in phase_regions.items():
        patch = patches.Polygon(coords, closed=True, facecolor=phase_colors[phase], alpha=0.7, label=f"Phase {phase}")
        patch.set_clip_path(triangle_patch, transform=ax.transData)
        ax.add_patch(patch)

    # Grid lines and composition labels
    for i in range(5, 100, 5):
        f = i / 100
        is_major = i % 10 == 0
        color = '#ffffff' if is_major else '#cccccc'  # More readable
        lw = 1.5 if is_major else 0.8
        ls = '-' if is_major else '--'
        fontsize = 8 if is_major else 6
        fontweight = 'bold' if is_major else 'normal'

        # Grid lines
        ax.plot([f/2, 1 - f/2], [f*np.sqrt(3)/2]*2, color=color, lw=lw, ls=ls)
        ax.plot([f, (1 + f)/2], [0, (1 - f)*np.sqrt(3)/2], color=color, lw=lw, ls=ls)
        ax.plot([(1 - f)/2, 1 - f], [(1 - f)*np.sqrt(3)/2, 0], color=color, lw=lw, ls=ls)

        # Composition Labels
        ax.text(f, -0.04, f"{100 - i}", ha='center', va='top', fontsize=fontsize, fontweight=fontweight, color=color)
        ax.text((1 + f)/2 + 0.03, (1 - f)*np.sqrt(3)/2, f"{i}", ha='left', fontsize=fontsize, fontweight=fontweight, color=color)
        ax.text((1 - f)/2 - 0.03, (1 - f)*np.sqrt(3)/2, f"{i}", ha='right', fontsize=fontsize, fontweight=fontweight, color=color)

    # Plot the user’s selected composition point
    ax.plot(x, y, 'ro', markersize=8)
    ax.text(x, y + 0.035, f"({A}, {B}, {C})", ha='center', fontsize=10, fontweight='bold', color='white')

    # Corner labels
    ax.text(-0.05, -0.05, "B (100%)", ha='right', fontsize=11, fontweight='bold', color='#00b4d8')
    ax.text(1.05, -0.05, "C (100%)", ha='left', fontsize=11, fontweight='bold', color='#57cc99')
    ax.text(0.5, np.sqrt(3)/2 + 0.05, "A (100%)", ha='center', fontsize=11, fontweight='bold', color='#f77f00')

    # Final formatting
    ax.set_aspect('equal')
    ax.axis('off')
    ax.legend(loc='lower center', ncol=3, fontsize=10, frameon=False)
    st.pyplot(fig)
