import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Ternary Diagram (Gibbs Triangle) Viewer")

# Input Sliders
A = st.slider("Component A (%)", 0, 100, 30)
B = st.slider("Component B (%)", 0, 100 - A, 30)
C = 100 - A - B

st.write(f"Component C (%) is automatically set to: **{C}**")

# Convert ternary coordinates to Cartesian
# A + B + C = 100 -> point inside equilateral triangle

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

# Draw grid lines (optional)
for i in range(1, 10):
    f = i / 10
    # Parallel to base (constant C)
    ax.plot([f/2, 1 - f/2], [f * np.sqrt(3)/2]*2, color='gray', linewidth=0.5, linestyle='--')
    # Parallel to left side (constant B)
    ax.plot([f, (1+f)/2], [0, (1-f)*np.sqrt(3)/2], color='gray', linewidth=0.5, linestyle='--')
    # Parallel to right side (constant A)
    ax.plot([(1-f)/2, 1-f], [(1-f)*np.sqrt(3)/2, 0], color='gray', linewidth=0.5, linestyle='--')

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
