import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io

st.header("Simple Gibbs Triangle (No Phase Lines, with Color Gradient)")

# User input: A and B sliders, C is auto-calculated
A = st.slider("Component A (%) [No Phase Lines]", 0, 100, step=5, value=50, key='A_simple')
B = st.slider("Component B (%) [No Phase Lines]", 0, 100 - A, step=5, value=35, key='B_simple')
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

    # Generate a grid of points inside the triangle
    resolution = 100  # Higher = smoother gradient, lower = faster
    points = []
    colors = []
    for a in range(resolution + 1):
        for b in range(resolution + 1 - a):
            c = resolution - a - b
            if c < 0:
                continue
            aa = a / resolution * 100
            bb = b / resolution * 100
            cc = c / resolution * 100
            x, y = ternary_to_cartesian(aa, bb, cc)
            # RGB color proportional to (A, B, C)
            color = (aa/100, bb/100, cc/100)
            points.append((x, y))
            colors.append(color)

    points = np.array(points)
    colors = np.array(colors)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_facecolor("white")

    # Plot the color gradient
    ax.scatter(points[:,0], points[:,1], c=colors, s=8, marker='s', linewidths=0)

    # Draw main triangle
    triangle_coords = np.array([B_vertex, C_vertex, A_vertex])
    ax.plot(*zip(*(triangle_coords.tolist() + [triangle_coords[0].tolist()])), color='black', lw=2)

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
    x, y = ternary_to_cartesian(A, B, C)
    ax.plot(x, y, 'ro', markersize=12)
    ax.text(x, y + 0.03, f"({A:.1f}, {B:.1f}, {C:.1f})", ha='center', fontsize=12, fontweight='bold', color='black')

    # Vertex labels
    ax.text(0.5, np.sqrt(3)/2 + 0.06, "A (100%)", ha='center', fontsize=18, fontweight='bold', color='orange')
    ax.text(-0.05, -0.05, "B (100%)", ha='right', fontsize=18, fontweight='bold', color='blue')
    ax.text(1.05, -0.05, "C (100%)", ha='left', fontsize=18, fontweight='bold', color='green')

    ax.set_aspect('equal', adjustable='datalim')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, np.sqrt(3)/2)
    ax.axis('off')

    st.pyplot(fig)

    st.success(f"Composition: A = {A:.1f}%, B = {B:.1f}%, C = {C:.1f}%")

    # Download Feature
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    st.download_button(
        label="Download diagram as PNG",
        data=buf.getvalue(),
        file_name="simple_ternary_diagram_gradient.png",
        mime="image/png"
    )
