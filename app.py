import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
from matplotlib.path import Path

st.title("📘 Ternary Diagram with Phase Regions")

st.markdown("""
Adjust A and B (in multiples of 5).  
Component C is calculated automatically.  
We'll show the **phase region** (α, β, γ) based on your selected composition.
""")

# Input
A = st.slider("Component A (%)", min_value=0, max_value=100, step=5, value=30)
B = st.slider("Component B (%)", min_value=0, max_value=100 - A, step=5, value=30)
C = 100 - A - B

# Convert ternary to cartesian
def ternary_to_cartesian(a, b, c):
    total = a + b + c
    x = 0.5 * (2 * b + c) / total
    y = (np.sqrt(3) / 2) * c / total
    return x, y

# Define phase regions as triangle areas (keeping them inside the ternary triangle)
phase_regions = {
    "α": [(0.0, 0.0), (0.4, 0.0), (0.2, 0.3)],
    "β": [(0.4, 0.0), (1.0, 0.0), (0.7, 0.6), (0.2, 0.3)],
    "γ": [(0.2, 0.3), (0.7, 0.6), (0.5, np.sqrt(3)/2)]
}

# Determine which phase the point falls in
def get_phase(x, y):
    for phase, coords in phase_regions.items():
        path = Path(coords)
        if path.contains_point((x, y)):
            return phase
    return "Unknown"

if A + B > 100:
    st.error(f"Invalid: A + B = {A + B} > 100")
else:
    C = 100 - A - B
    x, y = ternary_to_cartesian(A, B, C)
    current_phase = get_phase(x, y)
    st.success(f"Composition: A = {A}%, B = {B}%, C = {C}% → Phase: **{current_phase}**")

    # Plot
    fig, ax = plt.subplots(figsize=(7, 7))

    # Set background color for the dark theme
    ax.set_facecolor('#2e2e2e')  # Dark background

    # Draw background
    ax.add_patch(patches.Polygon([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]],
                                  closed=True, facecolor='#3c3c3c', edgecolor='k'))

    # Draw phase regions with dark theme colors
    colors = {'α': '#4f81bd', 'β': '#f58f82', 'γ': '#93d19b'}
    for phase, coords in phase_regions.items():
        patch = patches.Polygon(coords, closed=True, facecolor=colors[phase], alpha=0.7, label=f'Phase {phase}')
        ax.add_patch(patch)

    # Grid lines with dark theme adjustments
    for i in range(5, 100, 5):
        f = i / 100
        is_10 = (i % 10 == 0)
        color = '#d3d3d3' if is_10 else '#a5a5a5'
        lw = 1.5 if is_10 else 0.8
        ls = '-' if is_10 else '--'
        fontsize = 8 if is_10 else 6
        fontweight = 'bold' if is_10 else 'normal'

        ax.plot([f / 2, 1 - f / 2], [f * np.sqrt(3)/2]*2, color=color, lw=lw, ls=ls)
        ax.plot([f, (1 + f)/2], [0, (1 - f) * np.sqrt(3)/2], color=color, lw=lw, ls=ls)
        ax.plot([(1 - f)/2, 1 - f], [(1 - f) * np.sqrt(3)/2, 0], color=color, lw=lw, ls=ls)

        ax.text(f, -0.04, f"{100 - i}", ha='center', va='top', fontsize=fontsize, fontweight=fontweight, color=color)
        ax.text((1 + f)/2 + 0.03, (1 - f) * np.sqrt(3)/2, f"{i}", ha='left', fontsize=fontsize, fontweight=fontweight, color=color)
        ax.text((1 - f)/2 - 0.03, (1 - f) * np.sqrt(3)/2, f"{i}", ha='right', fontsize=fontsize, fontweight=fontweight, color=color)

    # Outer triangle (border)
    ax.plot([0, 1, 0.5, 0], [0, 0, np.sqrt(3)/2, 0], 'w', lw=2)

    # Point
    ax.plot(x, y, 'ro', markersize=8)
    ax.text(x, y + 0.035, f"({A}, {B}, {C})", ha='center', fontsize=10, fontweight='bold', color='white')

    # Corner labels
    ax.text(-0.05, -0.05, "B (100%)", ha='right', fontsize=11, fontweight='bold', color='#0077b6')
    ax.text(1.05, -0.05, "C (100%)", ha='left', fontsize=11, fontweight='bold', color='#009e60')
    ax.text(0.5, np.sqrt(3)/2 + 0.05, "A (100%)", ha='center', fontsize=11, fontweight='bold', color='#d62828')

    ax.set_aspect('equal')
    ax.axis('off')
    ax.legend(loc='lower center', ncol=3, fontsize=10, frameon=False, title="Phase Regions", title_fontsize=12, labelspacing=1.2)
    st.pyplot(fig)
