import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon
from IPython.display import HTML
import matplotlib

# Set backend for Streamlit
matplotlib.use('Agg')

st.title("Triangle with Projection Line Animation")

# Triangle vertices
A = np.array([0, 0])
B = np.array([5, 0])
C = np.array([2.5, 4.33])  # Equilateral triangle height ≈ 4.33

# Create figure and axis
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(-1, 6)
ax.set_ylim(-1, 5)
ax.set_aspect('equal')
ax.grid(True)

# Draw the triangle
triangle = Polygon([A, B, C], fill=False, edgecolor='black', linewidth=2)
ax.add_patch(triangle)

# Label the vertices
ax.text(A[0]-0.2, A[1]-0.2, 'A', fontsize=12)
ax.text(B[0]+0.2, B[1]-0.2, 'B', fontsize=12)
ax.text(C[0], C[1]+0.2, 'C', fontsize=12)

# Initialize moving point on AC and its projection line
point_on_AC, = ax.plot([], [], 'ro', markersize=8)
projection_line, = ax.plot([], [], 'b--', linewidth=1.5)
projection_foot, = ax.plot([], [], 'go', markersize=6)

# Function to find the foot of the perpendicular from point P to line BC
def find_perpendicular_foot(P, B, C):
    # Vector BC
    BC = C - B
    # Vector BP
    BP = P - B
    # Projection of BP onto BC
    t = np.dot(BP, BC) / np.dot(BC, BC)
    t = np.clip(t, 0, 1)  # Ensure the foot is within the segment BC
    foot = B + t * BC
    return foot

# Animation update function
def update(t):
    # Parameter t goes from 0 to 1
    # Calculate point position along AC
    P = A + t * (C - A)
    point_on_AC.set_data([P[0]], [P[1]])
    
    # Find the foot of the perpendicular from P to BC
    foot = find_perpendicular_foot(P, B, C)
    
    # Update projection line (from P to foot)
    projection_line.set_data([P[0], foot[0]], [P[1], foot[1]])
    projection_foot.set_data([foot[0]], [foot[1]])
    
    return point_on_AC, projection_line, projection_foot

# Create animation
ani = FuncAnimation(fig, update, frames=np.linspace(0, 1, 100),
                    interval=50, blit=True)

# Display in Streamlit
st.write("Animation showing a point moving along AC with its perpendicular projection to BC:")
st.pyplot(fig)

# To display the actual animation in Streamlit, we need to convert it to HTML
st.write("Animated version (may not display in all environments):")
components.html(ani.to_jshtml(), height=800)
