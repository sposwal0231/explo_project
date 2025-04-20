import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
from matplotlib.path import Path

st.title("📘 Ternary Phase Diagram")

st.markdown("""
Select values for **Component A** and **B** (in multiples of 5).  
**Component C** will be calculated automatically.  
The diagram shows which **phase region (α, β, γ)** your composition falls into.
""")

# Input sliders
A = st.slider("Component A (%)", min_value=0, max_value=100, step=5, value=30)
B = st.slider("Component B (%)", min_value=0, max_value=100 - A, step=5, value=30)
C = 100 - A - B

# Ternary to Cartesian converter
def ternary_to_cartesian(a, b, c):
    total = a + b + c
    x = 0.5 * (2 * b + c) / total
    y = (np.sqrt(3) / 2) * c / total
    return x, y

# Define sample phase regions (as polygons)
phase_regions = {
    "α": [(0.0, 0.0), (0.4, 0.0), (0.2, 0.3)],
    "β": [(0.4, 0.0), (1.0, 0.0), (0.7, 0.6), (0.2, 0.3)],
    "γ": [(0.2, 0.3), (0.7, 0.6), (0.5, np.sqrt(3)/2)]
}

# Determine which phase the point falls into
def get_phase(x, y):
    for phase, coords in phase_regions.items():
        path = Path(coords)
        if path.contains_point((x, y)):
            return phase
    return "Unknown"

# Check input
if A + B > 100:
    st.error("Invalid input: A + B exceeds 100.")
else:
    C = 100 - A - B
    x, y = ternary_to_cartesian(A, B, C)
    current_phase = get_phase(x, y)

    st.success(f"✅ Composition: A={A}%, B={B}%, C={C}% → Phase: **{current_phase}**")

    # Begin plotting
    fig, ax = plt.subplots(figsize=(8, 8))  # Bigger size

    # Base triangle background
    ax.add_patch(patches.Polygon([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]],
                                  closed=True, facecolor='#f9f9f9', edgecolor='black'))

    # Phase region shading (subtle)
    phase_colors = {'α': '#d0e1f9', 'β': '#fce1e4', 'γ': '#e0f9d7'}
    for phase, coords in phase_regions.items():
        ax.add_patch(patches.Polygon(coords, closed=True,
                                     facecolor=phase_colors[phase], alpha=0.6,
                                     edgecolor='gray', linewidth=0.8))

    # Draw grid lines
    for i in range(5, 100, 5):
        f = i / 100
        is_10 = (i % 10 == 0)
        color = '#333333' if is_10 else '#bbbbbb'
        lw = 1.2 if is_10 else 0.6
        ls = '-' if is_10 else '--'
        fontsize = 8 if is_10 else 6
        fontweight = 'bold' if is_10 else 'normal'

        # Lines
        ax.plot([f/2, 1 - f/2], [f * np.sqrt(3)/2]*2, color=color, lw=lw, ls=ls)  # A lines
        ax.plot([f, (1 + f)/2], [0, (1 - f)*np.sqrt(3)/2], color=color, lw=lw, ls=ls)  # B lines
        ax.plot([(1 - f)/2, 1 - f], [(1 - f)*np.sqrt(3)/2, 0], color=color, lw=lw, ls=ls)  # C lines

        # Labels
        ax.text(f, -0.04, f"{100 - i}", ha='center', va='top', fontsize=fontsize, fontweight=fontweight, color=color)
        ax.text((1 + f)/2 + 0.02, (1 - f)*np.sqrt(3)/2, f"{i}", ha='left', fontsize=fontsize, fontweight=fontweight, color=color)
        ax.text((1 - f)/2 - 0.02, (1 - f)*np.sqrt(3)/2, f"{i}", ha='right', fontsize=fontsize, fontweight=fontweight, color=color)

    # Outer triangle border
    triangle_coords = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2], [0, 0]])
    ax.plot(triangle_coords[:, 0], triangle_coords[:, 1], color="black", linewidth=2)

    # Composition point
    ax.plot(x, y, 'ro', markersize=8)
    ax.text(x, y + 0.035, f"({A}, {B}, {C})", ha='center', fontsize=10, fontweight='bold')

    # Corner labels - simple style
    ax.text(-0.05, -0.05, "B (100%)", ha='right', fontsize=10, fontweight='bold')
    ax.text(1.05, -0.05, "C (100%)", ha='left', fontsize=10, fontweight='bold')
    ax.text(0.5, np.sqrt(3)/2 + 0.05, "A (100%)", ha='center', fontsize=10, fontweight='bold')

    ax.set_aspect('equal')
    ax.axis('off')
    ax.legend([patches.Patch(color=c, label=f'Phase {p}') for p, c in phase_colors.items()],
              loc='lower center', ncol=3, fontsize=9)
    st.pyplot(fig)
