import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
from matplotlib.path import Path
import io

st.title("Ternary Diagram with Dynamic Highlighting and Download")

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

# Example: Three arbitrary phase regions (triangle-based for clarity)
region_alpha = [B_vertex, (0.35, 0.2), (0.2, 0.5), A_vertex]
region_beta = [(0.35, 0.2), (0.7, 0.2), (0.8, 0.5), (0.2, 0.5)]
region_gamma = [(0.7, 0.2), C_vertex, A_vertex, (0.8, 0.5)]

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
highlight_colors = {
    "α": "#3366ff",    # strong blue
    "β": "#33cc33",    # strong green
    "γ": "#ff3333"     # strong red
}

def get_phase(x, y):
    for phase, coords in phase_regions.items():
        path = Path(coords)
        if path.contains_point((x, y)):
            return phase
    return "Unknown"

x, y = ternary_to_cartesian(A, B, C)
phase = get_phase(x, y)

fig, ax = plt.subplots(figsize=(7, 7))
ax.set_facecolor("white")

# Draw main triangle
triangle_coords = np.array([B_vertex, C_vertex, A_vertex])
triangle_patch = patches.Polygon(triangle_coords, closed=True, facecolor="white", edgecolor='black', lw=2)
ax.add_patch(triangle_patch)

# Draw phase regions with dynamic highlighting
for p, coords in phase_regions.items():
    color = highlight_colors[p] if p == phase else phase_colors[p]
    alpha = 0.7 if p == phase else 0.2
    phase_patch = patches.Polygon(coords, closed=True, facecolor=color, edgecolor='black', lw=2, alpha=alpha, zorder=1)
    phase_patch.set_clip_path(triangle_patch)
    ax.add_patch(phase_patch)

# Draw phase boundaries
for coords in phase_regions.values():
    ax.plot(*zip(*(coords + [coords[0]])), color='black', lw=2)

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
ax.plot(x, y, 'ro', markersize=10, zorder=2)
ax.text(x, y + 0.035, f"({A}, {B}, {C})", ha='center', fontsize=11, fontweight='bold', color='black', zorder=3)

# Vertex labels
ax.text(0.5, np.sqrt(3)/2 + 0.05, "A (100%)", ha='center', fontsize=13, fontweight='bold', color='orange')
ax.text(-0.05, -0.05, "B (100%)", ha='right', fontsize=13, fontweight='bold', color='blue')
ax.text(1.05, -0.05, "C (100%)", ha='left', fontsize=13, fontweight='bold', color='green')

# Add legend for phase colors
legend_patches = [
    patches.Patch(color=highlight_colors["α"], label="Phase α (highlighted)"),
    patches.Patch(color=highlight_colors["β"], label="Phase β (highlighted)"),
    patches.Patch(color=highlight_colors["γ"], label="Phase γ (highlighted)")
]
ax.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=3, frameon=True)

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
