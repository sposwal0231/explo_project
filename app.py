import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

st.title("🎨 Stylish Ternary Diagram (Gibbs Triangle) Plotter")

st.markdown("""
Adjust the sliders to set **Component A** and **Component B** (in steps of 5).  
Component **C** is automatically calculated as `100 - A - B`.
""")

# Input sliders
A = st.slider("Component A (%)", min_value=0, max_value=100, step=5, value=30)
B = st.slider("Component B (%)", min_value=0, max_value=100 - A, step=5, value=30)
C = 100 - A - B

if A + B > 100:
    st.error(f"The sum of A and B cannot exceed 100. Current sum: {A + B}")
else:
    st.success(f"🎯 Valid input! Component C is: {C}%")

    # Ternary to Cartesian
    def ternary_to_cartesian(a, b, c):
        total = a + b + c
        x = 0.5 * (2 * b + c) / total
        y = (np.sqrt(3) / 2) * c / total
        return x, y

    fig, ax = plt.subplots(figsize=(7, 7))

    # Add soft gradient background with pastel feel
    bg_triangle = patches.Polygon(
        [[0, 0], [1, 0], [0.5, np.sqrt(3)/2]],
        closed=True,
        facecolor="#fef6e4",  # soft cream
        edgecolor='none',
        alpha=0.9
    )
    ax.add_patch(bg_triangle)

    # Outer triangle border
    triangle_coords = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2], [0, 0]])
    ax.plot(triangle_coords[:, 0], triangle_coords[:, 1], color="#333333", linewidth=2)

    # Draw grid
    for i in range(5, 100, 5):
        f = i / 100
        is_multiple_10 = (i % 10 == 0)
        color = '#003f5c' if is_multiple_10 else '#ffa600'  # navy vs orange
        linewidth = 1.5 if is_multiple_10 else 0.8
        linestyle = '-' if is_multiple_10 else '--'
        fontsize = 8 if is_multiple_10 else 6
        fontweight = 'bold' if is_multiple_10 else 'normal'

        # Grid lines
        ax.plot([f/2, 1 - f/2], [f * np.sqrt(3)/2]*2, color=color, linewidth=linewidth, linestyle=linestyle)  # A lines
        ax.plot([f, (1 + f)/2], [0, (1 - f) * np.sqrt(3)/2], color=color, linewidth=linewidth, linestyle=linestyle)  # B lines
        ax.plot([(1 - f)/2, 1 - f], [(1 - f) * np.sqrt(3)/2, 0], color=color, linewidth=linewidth, linestyle=linestyle)  # C lines

        # Grid labels
        ax.text(f, -0.04, f"{100 - i}", ha='center', va='top', fontsize=fontsize, fontweight=fontweight, color=color)
        ax.text((1 + f)/2 + 0.03, (1 - f) * np.sqrt(3)/2, f"{i}", ha='left', va='center', fontsize=fontsize, fontweight=fontweight, color=color)
        ax.text((1 - f)/2 - 0.03, (1 - f) * np.sqrt(3)/2, f"{i}", ha='right', va='center', fontsize=fontsize, fontweight=fontweight, color=color)

    # Plot the user point
    x, y = ternary_to_cartesian(A, B, C)
    ax.plot(x, y, 'ro', markersize=8)
    ax.text(x, y + 0.035, f"({A}, {B}, {C})", ha='center', fontsize=10, fontweight='bold', color='black')

    # Corner labels
    ax.text(-0.05, -0.05, "B (100%)", ha='right', fontsize=11, fontweight='bold', color='#0077b6')
    ax.text(1.05, -0.05, "C (100%)", ha='left', fontsize=11, fontweight='bold', color='#009e60')
    ax.text(0.5, np.sqrt(3)/2 + 0.05, "A (100%)", ha='center', fontsize=11, fontweight='bold', color='#d62828')

    ax.set_aspect('equal')
    ax.axis('off')

    st.pyplot(fig)
