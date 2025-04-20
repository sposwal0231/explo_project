import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
from matplotlib.path import Path

st.set_page_config(layout="centered")
st.title("Ternary Phase Diagram")

st.markdown("""
🎯 **Adjust Component A and B** (multiples of 5).  
Component **C** is automatically `100 - A - B`.  
The plot shows the **phase region** based on the composition.
""")

# Sliders
A = st.slider("Component A (%)", 0, 100, 30, step=5)
B = st.slider("Component B (%)", 0, 100 - A, 30, step=5)
C = 100 - A - B

# Convert to Cartesian
def ternary_to_cartesian(a, b, c):
    total = a + b + c
    x = 0.5 * (2 * b + c) / total
    y = (np.sqrt(3)/2) * c / total
    return x, y

# Triangle vertices
triangle = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]])

# Phase regions (inside triangle)
phase_regions = {
    "α": [(0.05, 0.05), (0.35, 0.05), (0.2, 0.25)],
    "β": [(0.35, 0.05), (0.9, 0.05), (0.6, 0.45), (0.2, 0.25)],
    "γ": [(0.2, 0.25), (0.6, 0.45), (0.5, np.sqrt(3)/2 - 0.05)]
}

# Determine which phase point falls in
def get_phase(x, y):
    for phase, coords in phase_regions.items():
        path = Path(coords)
        if path.contains_point((x, y)):
            return phase
    return "Unknown"

# Create figure
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')
ax.axis('off')

# Black background triangle
ax.add_patch(patches.Polygon(triangle, closed=True, edgecolor='white', facecolor='black', linewidth=2))

# Phase region colors
phase_colors = {'α': '#2E86DE', 'β': '#E74C3C', 'γ': '#27AE60'}

# Draw and clip phase regions inside triangle
for phase, coords in phase_regions.items():
    patch = patches.Polygon(coords, closed=True, facecolor=phase_colors[phase], edgecolor='white', linewidth=0.5, alpha=0.6)
    patch.set_clip_path(patches.Polygon(triangle, closed=True))
    ax.add_patch(patch)

# Draw grid lines and labels
for i in range(5, 100, 5):
    f = i / 100
    bold = (i % 10 == 0)
    color = 'white' if bold else '#888'
    lw = 1.5 if bold else 0.6
    ls = '-' if bold else '--'
    fs = 8 if bold else 6
    fw = 'bold' if bold else 'normal'

    # Gridlines
    ax.plot([f/2, 1 - f/2], [f * np.sqrt(3)/2]*2, color=color, lw=lw, ls=ls)
    ax.plot([f, (1 + f)/2], [0, (1 - f)*np.sqrt(3)/2], color=color, lw=lw, ls=ls)
    ax.plot([(1 - f)/2, 1 - f], [(1 - f)*np.sqrt(3)/2, 0], color=color, lw=lw, ls=ls)

    # Labels
    ax.text(f, -0.035, f"{100 - i}", ha='center', fontsize=fs, fontweight=fw, color=color)
    ax.text((1 + f)/2 + 0.02, (1 - f)*np.sqrt(3)/2, f"{i}", ha='left', fontsize=fs, fontweight=fw, color=color)
    ax.text((1 - f)/2 - 0.02, (1 - f)*np.sqrt(3)/2, f"{i}", ha='right', fontsize=fs, fontweight=fw, color=color)

# Corner labels
ax.text(-0.05, -0.05, "B (100%)", ha='right', fontsize=10, fontweight='bold', color='white')
ax.text(1.05, -0.05, "C (100%)", ha='left', fontsize=10, fontweight='bold', color='white')
ax.text(0.5, np.sqrt(3)/2 + 0.05, "A (100%)", ha='center', fontsize=10, fontweight='bold', color='white')

# Plot the selected point
x, y = ternary_to_cartesian(A, B, C)
ax.plot(x, y, 'ro', markersize=8)
ax.text(x, y + 0.035, f"({A}, {B}, {C})", ha='center', fontsize=10, fontweight='bold', color='white')

# Legend
legend_handles = [patches.Patch(color=col, label=f"Phase {ph}") for ph, col in phase_colors.items()]
ax.legend(handles=legend_handles, loc='lower center', ncol=3, fontsize=9, facecolor='black', edgecolor='white', labelcolor='white')

# Show plot
st.pyplot(fig)

# Determine phase
phase = get_phase(x, y)
st.success(f"✅ The composition ({A}%, {B}%, {C}%) falls in **Phase {phase}**")
