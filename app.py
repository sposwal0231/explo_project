import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
import matplotlib.patches as mpatches
from matplotlib.path import Path
import io

st.title("Gibb's Triangle with Phase Regions")

# User sets A, then B is restricted so A+B<=100
A = st.slider("Component A (%)", 0, 100, step=5, value=50)
B = st.slider("Component B (%)", 0, 100 - A, step=5, value=35)
C = 100 - A - B

if C < 0:
    st.error(f"Invalid composition: C is negative (A+B={A+B} > 100). Please adjust A and B so their sum is ≤ 100.")
else:
    def ternary_to_cartesian(a, b, c):
        total = a + b + c
        x = 0.5 * (2 * c + a) / total
        y = (np.sqrt(3) / 2) * a / total
        return x, y

    # Triangle vertices
    A_vertex = (0.5, np.sqrt(3)/2)
    B_vertex = (0, 0)
    C_vertex = (1, 0)

    # Intersection points for phase boundaries (estimated visually)
    intersection = ternary_to_cartesian(40, 40, 20)
    left_boundary = ternary_to_cartesian(70, 30, 0)
    bottom_boundary = ternary_to_cartesian(0, 20, 80)

    # Phase boundaries (for bold lines)
    boundary1 = [left_boundary, intersection]
    boundary2 = [intersection, bottom_boundary]
    boundary3 = [B_vertex, intersection]

    # Phase region polygons (no overlap)
    region_alpha = [B_vertex, intersection, A_vertex, left_boundary]
    region_beta  = [intersection, bottom_boundary, C_vertex, A_vertex, left_boundary]
    region_gamma = [B_vertex, intersection, bottom_boundary, C_vertex]

    phase_regions = {
        "α": region_alpha,
        "β": region_beta,
        "γ": region_gamma
    }
    phase_colors = {
        "α": "#ffcccc",
        "β": "#d6f5d6",
        "γ": "#d6e0f5"
    }

    def get_phase(x, y):
        for phase, coords in phase_regions.items():
            path = Path(coords)
            if path.contains_point((x, y)):
                return phase
        return "Unknown"

    x, y = ternary_to_cartesian(A, B, C)
    phase = get_phase(x, y)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_facecolor("white")

    # Draw phase regions
    for p, coords in phase_regions.items():
        phase_patch = patches.Polygon(coords, closed=True, facecolor=phase_colors[p], edgecolor=None, lw=0, alpha=0.7, zorder=1)
        ax.add_patch(phase_patch)

    # Draw bold black phase boundaries
    ax.plot(*zip(*boundary1), color='black', lw=3, zorder=2)
    ax.plot(*zip(*boundary2), color='black', lw=3, zorder=2)
    ax.plot(*zip(*boundary3), color='black', lw=3, zorder=2)

    # Draw main triangle
    triangle_coords = np.array([B_vertex, C_vertex, A_vertex])
    ax.plot(*zip(*(triangle_coords.tolist() + [triangle_coords[0].tolist()])), color='black', lw=2, zorder=3)

    # Draw grid lines and grid triangles
    for i in range(5, 100, 5):
        f = i / 100
        is_major = i % 10 == 0
        color = '#404040' if is_major else '#808080'
        lw = 2 if is_major else 1.5
        fontsize = 10 if is_major else 8
        fontweight = 'bold' if is_major else 'normal'
        # Horizontal grid
        ax.plot([f/2, 1 - f/2], [f*np.sqrt(3)/2]*2, color=color, lw=lw, ls='-')
        # Right grid
        ax.plot([f, (1 + f)/2], [0, (1 - f)*np.sqrt(3)/2], color=color, lw=lw, ls='-')
        # Left grid
        ax.plot([(1 - f)/2, 1 - f], [(1 - f)*np.sqrt(3)/2, 0], color=color, lw=lw, ls='-')
        # Axis labels
        ax.text(f, -0.04, f"{100 - i}", ha='center', va='top', fontsize=fontsize, fontweight=fontweight, color=color)
        ax.text((1 + f)/2 + 0.03, (1 - f)*np.sqrt(3)/2, f"{i}", ha='left', fontsize=fontsize, fontweight=fontweight, color=color)
        ax.text((1 - f)/2 - 0.03, (1 - f)*np.sqrt(3)/2, f"{100- i}", ha='right', fontsize=fontsize, fontweight=fontweight, color=color)

    # User point
    ax.plot(x, y, 'ro', markersize=12, zorder=4)
    ax.text(x, y + 0.03, f"({A:.1f}, {B:.1f}, {C:.1f})", ha='center', fontsize=12, fontweight='bold', color='black', zorder=5)

    # Vertex labels
    ax.text(0.5, np.sqrt(3)/2 + 0.06, "A (100%)", ha='center', fontsize=18, fontweight='bold', color='orange')
    ax.text(-0.05, -0.05, "B (100%)", ha='right', fontsize=18, fontweight='bold', color='blue')
    ax.text(1.05, -0.05, "C (100%)", ha='left', fontsize=18, fontweight='bold', color='green')

    # Add legend for phase regions
    legend_patches = [
        mpatches.Patch(color="#ffcccc", label="Phase α (red, top)"),
        mpatches.Patch(color="#d6f5d6", label="Phase β (green, bottom right)"),
        mpatches.Patch(color="#d6e0f5", label="Phase γ (blue, bottom left)")
    ]
    ax.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=3, frameon=True)

    ax.set_aspect('equal', adjustable='datalim')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, np.sqrt(3)/2)
    ax.axis('off')

    st.pyplot(fig)

    # Show result message
    st.success(f"Composition: A = {A:.1f}%, B = {B:.1f}%, C = {C:.1f}% → Phase: **{phase}**")

    # Download Feature
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    st.download_button(
        label="Download diagram as PNG",
        data=buf.getvalue(),
        file_name="ternary_diagram.png",
        mime="image/png"
    )
