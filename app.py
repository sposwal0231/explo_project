import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

st.title("🌈 Enhanced Ternary Diagram (Gibbs Triangle) Plotter")

st.markdown("""
Use the sliders to adjust **Component A** and **Component B** (multiples of 5).
Component **C** is auto-calculated as `100 - A - B`.
""")

# Input sliders
A = st.slider("Component A (%)", min_value=0, max_value=100, step=5, value=30)
B = st.slider("Component B (%)", min_value=0, max_value=100 - A, step=5, value=30)
C = 100 - A - B

if A + B > 100:
    st.error(f"The sum of A and B cannot exceed 100. Current sum: {A + B}")
else:
    st.success(f"✅ Valid input! Component C is: {C}%")

    # Coordinate converter
    def ternary_to_cartesian(a, b, c):
        total = a + b + c
        x = 0.5 * (2 * b + c) / total
        y = (np.sqrt(3) / 2) * c / total
        return x, y

    fig, ax = plt.subplots(figsize=(7, 7))

    # Gradient background triangle using a filled polygon
    gradient_colors = ["#f0f8ff", "#e0ffff", "#ffe4e1"]
    triangle = patches.Polygon(
        [[0, 0], [1, 0], [0.5, np.sqrt(3)/2]], closed=True,
        facecolor="whitesmoke", edgecolor='none', alpha=0.25
    )
    ax.add_patch(triangle)

    # Outer triangle
    triangle_coords = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2], [0, 0]])
    ax.plot(triangle_coords[:, 0], triangle_coords[:, 1], 'k', linewidth=2)

    # Draw grid
    for i in range(5, 100, 5):
        f = i / 100
        is_multiple_10 = (i % 10 == 0)
        color = 'darkblue' if is_multiple_10 else 'lightgray'
        linewidth = 1.2 if is_multiple_10 else 0.5
        linestyle = '-' if is_multiple_10 else '--'
        fontsize = 8 if is_multiple_10 else 6
        fontweight = 'bold' if is_multiple_10 else 'normal'

        # Horizontal (A lines)
        ax.plot([f/2, 1 - f/2], [f * np.sqrt(3)/2] * 2, color=color, linewidth=linewidth, linestyle=linestyle)
        # Diagonal from B to A (C lines)
        ax.plot([f, (1 + f)/2], [0, (1 - f) * np.sqrt(3)/2], color=color, linewidth=linewidth, linestyle=linestyle)
        # Diagonal from C to B (B lines)
        ax.plot([(1 - f)/2, 1 - f], [(1 - f) * np.sqrt(3)/2, 0], color=color, linewidth=linewidth, linestyle=linestyle)

        # Labels
        ax.text(f, -0.04, f"{100 - i}", ha='center', va='top', fontsize=fontsize, fontweight=fontweight, color=color)
        ax.text((1 + f)/2 + 0.03, (1 - f) * np.sqrt(3)/2, f"{i}", ha='left', va='center', fontsize=fontsize, fontweight=fontweight, color=color)
        ax.text((1 - f)/2 - 0.03, (1 - f) * np.sqrt(3)/2, f"{i}", ha='right', va='center', fontsize=fontsize, fontweight=fontweight, color=color)

    # Plot the point
    x, y = ternary_to_cartesian(A, B, C)
    ax.plot(x, y, 'ro', markersize=8)
    ax.text(x, y + 0.03, f"({A}, {B}, {C})", ha='center', fontsize=10, fontweight='bold')

    # Corner labels
    ax.text(-0.05, -0.05, "B (100%)", ha='right', fontsize=10, fontweight='bold', color='blue')
    ax.text(1.05, -0.05, "C (100%)", ha='left', fontsize=10, fontweight='bold', color='green')
    ax.text(0.5, np.sqrt(3)/2 + 0.05, "A (100%)", ha='center', fontsize=10, fontweight='bold', color='red')

    ax.set_aspect('equal')
    ax.axis('off')

    st.pyplot(fig)
