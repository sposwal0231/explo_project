import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
import io

st.title("Ternary Diagram with Phase Regions and Download")

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

# Define phase boundary lines (as in your image)
boundary1 = [ternary_to_cartesian(70, 30, 0), ternary_to_cartesian(20, 60, 20)]
boundary2 = [ternary_to_cartesian(20, 60, 20), ternary_to_cartesian(0, 20, 80)]

# Phase region polygons (manually traced from your image)
region_alpha = [B_vertex, ternary_to_cartesian(70, 30, 0), ternary_to_cartesian(20, 60, 20)]
region_beta = [ternary_to_cartesian(70, 30, 0), A_vertex, C_vertex, ternary_to_cartesian(0, 20, 80), ternary_to_cartesian(20, 60, 20)]
region_gamma = [B_vertex, ternary_to_cartesian(20, 60, 20), ternary_to_cartesian(0, 20, 80), C_vertex]

phase_regions = {
    "α": region_alpha,
    "β": region_beta,
    "γ": region_gamma
}
phase_colors = {
    "α": "#b3c6ff",    # light blue
    "β": "#b3ffb3",    # light green
    "γ": "#ffb3b3"     # light coral
}

def get_phase(x, y):
    from matplotlib.path import Path
    for phase, coords in phase_regions.items():
        path = Path(coords)
        if path.contains_point((x, y)):
            return phase
    return "Unknown"

x, y = ternary_to_cartesian(A, B, C)
phase = get_phase(x, y)

fig, ax = plt.subplots(figsize=(7, 7))
ax.set_facecolor("white")

# Draw phase regions
for p, coords in phase_regions.items():
    phase_patch = patches.Polygon(coords, closed=True, facecolor=phase_colors[p], edgecolor=None, lw=0, alpha=0.4, zorder=1)
    ax.add_patch(phase_patch)

# Draw bold black phase boundaries
ax.plot(*zip(*boundary1), color='black', lw=3, zorder=2)
ax.plot(*zip(*boundary2), color='black', lw=3, zorder=2)

# Draw main triangle
triangle_coords = np.array([B_vertex, C_vertex, A_vertex])
triangle_patch = patches.Polygon(triangle_coords, closed=True, facecolor="none", edgecolor='black', lw=2)
ax.add_patch(triangle_patch)
ax.plot(*zip(*(triangle_coords.tolist() + [triangle_coords[0].tolist()])), color='black', lw=2, zorder=3)

# Draw grid lines
for i in range(5, 100, 5):
    f = i / 100
    is_major = i % 10 == 0
    color = '#404040' if is_major else '#808080'
    lw = 2 if is_major else 1.5
    fontsize = 10 if is_major else 8
    fontweight = 'bold' if is_major else 'normal'

    ax.plot([f/2, 1 - f/2], [f*np.sqrt(3)/2]*2, color=color, lw=lw, ls='-')
    ax.plot([f, (1 + f)/2], [0, (1 - f)*np.sqrt(3)/2], color=color, lw=lw, ls='-')
    ax.plot([(1 - f)/2, 1 - f], [(1 - f)*np.sqrt(3)/2, 0], color=color, lw=lw, ls='-')

    ax.text(f, -0.04, f"{100 - i}", ha='center', va='top', fontsize=fontsize, fontweight=fontweight, color=color)
    ax.text((1 + f)/2 + 0.03, (1 - f)*np.sqrt(3)/2, f"{100 - i}", ha='left', fontsize=fontsize, fontweight=fontweight, color=color)
    ax.text((1 - f)/2 - 0.03, (1 - f)*np.sqrt(3)/2, f"{100 - i}", ha='right', fontsize=fontsize, fontweight=fontweight, color=color)

# User point
ax.plot(x, y, 'ro', markersize=12, zorder=4)
ax.text(x, y + 0.035, f"({A}, {B}, {C})", ha='center', fontsize=12, fontweight='bold', color='black', zorder=5)

# Vertex labels
ax.text(0.5, np.sqrt(3)/2 + 0.05, "A (100%)", ha='center', fontsize=15, fontweight='bold', color='orange')
ax.text(-0.05, -0.05, "B (100%)", ha='right', fontsize=15, fontweight='bold', color='blue')
ax.text(1.05, -0.05, "C (100%)", ha='left', fontsize=15, fontweight='bold', color='green')

ax.set_aspect('equal', adjustable='datalim')
ax.set_xlim(0, 1)
ax.set_ylim(0, np.sqrt(3)/2)
ax.axis('off')

st.pyplot(fig)

# --- Download Feature ---
buf = io.BytesIO()
fig.savefig(buf, format="png", bbox_inches="tight")
st.download_button(
    label="Download diagram as PNG",
    data=buf.getvalue(),
    file_name="ternary_diagram.png",
    mime="image/png"
)
