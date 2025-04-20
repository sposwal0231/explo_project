import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
from matplotlib.path import Path

st.set_page_config(layout="wide")
st.title("📘 Ternary Phase Diagram")

st.markdown("""
Adjust **Component A** and **Component B** (multiples of 5).  
Component **C** is auto-calculated as `100 - A - B`.  
The diagram shows which **phase region (α, β, γ)** your composition falls into.
""")

# Sliders for A and B
A = st.slider("Component A (%)", 0, 100, 30, step=5)
B = st.slider("Component B (%)", 0, 100 - A, 30, step=5)
C = 100 - A - B

# Convert ternary to 2D Cartesian
def ternary_to_cartesian(a, b, c):
    total = a + b + c
    x = 0.5 * (2 * b + c) / total
    y = (np.sqrt(3) / 2) * c / total
    return x, y

# Phase region definitions (simplified example polygons)
phase_regions = {
    "α": [(0.0, 0.0), (0.4, 0.0), (0.2, 0.3)],
    "β": [(0.4, 0.0), (1.0, 0.0), (0.7, 0.6), (0.2, 0.3)],
    "γ": [(0.2, 0.3), (0.7, 0.6), (0.5, np.sqrt(3)/2)]
}

# Check which phase the point is in
def get_phase(x, y):
    for phase, coords in phase_regions.items():
        path = Path(coords)
        if path.contains_point((x, y)):
            return phase
    return "Unknown"

# Draw ternary diagram
fig, ax = plt.subplots(figsize=(9, 9))
ax.set_aspect('equal')
ax.axis('off')

# Draw triangle background
triangle = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]])
ax.add_patch(patches.Polygon(triangle, closed=True, edgecolor='black', facecolor='#f9f9f9'))

# Draw phase regions
phase_colors = {'α': '#d0e1f9', 'β': '#fce1e4', 'γ': '#e0f9d7'}
for phase, coords in phase_regions.items():
    polygon = patches.Polygon(coords, closed=True, facecolor=phase_colors[phase],
                              edgecolor='gray', linewidth=1.0, alpha=0.6, label=f"Phase {phase}")
    ax.add_patch(polygon)

# Draw gridlines and labels
for i in range(5, 100, 5):
    f = i / 100
    bold = i % 10 == 0
    color = '#333' if bold else '#ccc'
    lw = 1.5 if bold else 0.6
    ls = '-' if bold else '--'
    fs = 8 if bold else 6
    fw = 'bold' if bold else 'normal'

    # Gridlines
    ax.plot([f / 2, 1 - f / 2], [f * np.sqrt(3)/2]*2, color=color, lw=lw, ls=ls)  # A-lines
    ax.plot([f, (1 + f)/2], [0, (1 - f)*np.sqrt(3)/2], color=color, lw=lw, ls=ls)  # B-lines
    ax.plot([(1 - f)/2, 1 - f], [(1 - f)*np.sqrt(3)/2, 0], color=color, lw=lw, ls=ls)  # C-lines

    # Labels
    ax.text(f, -0.04, f"{100 - i}", ha='center', fontsize=fs, fontweight=fw, color=color)         # B-C edge
    ax.text((1 + f)/2 + 0.02, (1 - f) * np.sqrt(3)/2, f"{i}", ha='left', fontsize=fs, fontweight=fw, color=color)  # A-C
    ax.text((1 - f)/2 - 0.02, (1 - f) * np.sqrt(3)/2, f"{i}", ha='right', fontsize=fs, fontweight=fw, color=color) # A-B

# Composition point
x, y = ternary_to_cartesian(A, B, C)
ax.plot(x, y, 'ro', markersize=10)
ax.text(x, y + 0.035, f"({A}, {B}, {C})", ha='center', fontsize=10, fontweight='bold')

# Corner labels
ax.text(-0.05, -0.05, "B (100%)", ha='right', fontsize=10, fontweight='bold')
ax.text(1.05, -0.05, "C (100%)", ha='left', fontsize=10, fontweight='bold')
ax.text(0.5, np.sqrt(3)/2 + 0.05, "A (100%)", ha='center', fontsize=10, fontweight='bold')

# Legend
handles = [patches.Patch(color=col, label=f"Phase {ph}") for ph, col in phase_colors.items()]
ax.legend(handles=handles, loc='lower center', ncol=3, fontsize=9)

# Show plot and phase
st.pyplot(fig)
st.success(f"Composition falls in **Phase {get_phase(x, y)}**")
