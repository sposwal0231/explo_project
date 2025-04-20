import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Ternary Diagram (Gibbs Triangle) Plotter")

st.markdown("""
Provide values for components A and B using sliders in multiples of 5. Component C will be calculated as 100 - A - B.
""")

# Input sliders for A and B (restricted to multiples of 5)
A = st.slider("Component A (%)", min_value=0, max_value=100, step=5, value=30)
B = st.slider("Component B (%)", min_value=0, max_value=100 - A, step=5, value=30)
C = 100 - A - B

if A + B > 100:
    st.error(f"The sum of A and B cannot exceed 100. Current sum: {A + B}")
else:
    st.success(f"Valid input! Component C is automatically calculated as: {C}%")

    # Convert ternary coordinates to Cartesian
    def ternary_to_cartesian(a, b, c):
        total = a + b + c
        x = 0.5 * (2 * b + c) / total
        y = (np.sqrt(3) / 2) * c / total
        return x, y

    # Create triangle background
    fig, ax = plt.subplots(figsize=(6, 6))

    # Draw outer triangle
    triangle_coords = np.array([
        [0, 0],
        [1, 0],
        [0.5, np.sqrt(3)/2],
        [0, 0]
    ])
    ax.plot(triangle_coords[:,0], triangle_coords[:,1], 'k')

    # Draw grid lines and labels for multiples of 5
    for i in range(5, 100, 5):
        f = i / 100
        # Grid lines
        ax.plot([f/2, 1 - f/2], [f * np.sqrt(3)/2]*2, color='gray', linewidth=0.5, linestyle='--')
        ax.plot([f, (1+f)/2], [0, (1-f)*np.sqrt(3)/2], color='gray', linewidth=0.5, linestyle='--')
        ax.plot([(1-f)/2, 1-f], [(1-f)*np.sqrt(3)/2, 0], color='gray', linewidth=0.5, linestyle='--')

        # Labels
        # B-C edge (bottom)
        ax.text(f, -0.03, f"{100 - i}", ha='center', va='top', fontsize=7)
        # A-C edge (right)
        x_ac = (1 + f) / 2
        y_ac = (1 - f) * np.sqrt(3)/2
        ax.text(x_ac + 0.03, y_ac, f"{i}", ha='left', va='center', fontsize=7)
        # A-B edge (left)
        x_ab = (1 - f) / 2
        y_ab = (1 - f) * np.sqrt(3)/2
        ax.text(x_ab - 0.03, y_ab, f"{i}", ha='right', va='center', fontsize=7)

    # Plot the point
    x, y = ternary_to_cartesian(A, B, C)
    ax.plot(x, y, 'ro')
    ax.text(x, y + 0.03, f"({A}, {B}, {C})", ha='center', fontsize=9)

    # Label corners
    ax.text(-0.05, -0.05, "B (100%)", ha='right')
    ax.text(1.05, -0.05, "C (100%)", ha='left')
    ax.text(0.5, np.sqrt(3)/2 + 0.05, "A (100%)", ha='center')

    ax.set_aspect('equal')
    ax.axis('off')

    st.pyplot(fig)
