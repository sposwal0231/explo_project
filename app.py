import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

st.title("Ternary Diagram with Phase Boundaries")

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

# Example phase boundary lines (edit these as you wish)
phase_line1 = [  # e.g. a line from (A=70,B=30,C=0) to (A=20,B=60,C=20)
    ternary_to_cartesian(70, 30, 0),
    ternary_to_cartesian(20, 60, 20)
]
phase_line2 = [  # e.g. a line from (A=20,B=60,C=20) to (A=0,B=20,C=80)
    ternary_to_cartesian(20, 60, 20),
    ternary_to_cartesian(0, 20, 80)
]

fig, ax = plt.subplots(figsize=(7, 7))
ax.set_facecolor("white")

# Draw main triangle
triangle_coords = np.array([B_vertex, C_vertex, A_vertex])
triangle_patch = patches.Polygon(triangle_coords, closed=True, facecolor="white", edgecolor='black', lw=2)
ax.add_patch(triangle_patch)

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

# Draw phase boundary lines
ax.plot(*zip(*phase_line1), color='black', lw=4, ls='-', label='Phase boundary 1')
ax.plot(*zip(*phase_line2), color='black', lw=4, ls='-', label='Phase boundary 2')

# User point
x, y = ternary_to_cartesian(A, B, C)
ax.plot(x, y, 'ro', markersize=10)
ax.text(x, y + 0.035, f"({A}, {B}, {C})", ha='center', fontsize=11, fontweight='bold', color='black')

# Vertex labels
ax.text(0.5, np.sqrt(3)/2 + 0.05, "A (100%)", ha='center', fontsize=13, fontweight='bold', color='orange')
ax.text(-0.05, -0.05, "B (100%)", ha='right', fontsize=13, fontweight='bold', color='blue')
ax.text(1.05, -0.05, "C (100%)", ha='left', fontsize=13, fontweight='bold', color='green')

ax.set_aspect('equal', adjustable='datalim')
ax.set_xlim(0, 1)
ax.set_ylim(0, np.sqrt(3)/2)
ax.axis('off')
ax.legend(loc='upper right')
st.pyplot(fig)
