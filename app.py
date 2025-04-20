import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
from matplotlib.path import Path

# Title and description
st.title("Ternary Diagram with Arbitrary Phase Boundaries")
st.markdown("""
Adjust components **A** and **B**. Component **C** is calculated automatically.  
Your selected composition will be placed on the triangle and the corresponding **phase region** will be shown.
""")

# Component sliders
A = st.slider("Component A (%)", 0, 100, step=5, value=50)
B = st.slider("Component B (%)", 0, 100 - A, step=5, value=30)
C = 100 - A - B

def ternary_to_cartesian(a, b, c):
    total = a + b + c
    # A at top, B at bottom left, C at bottom right
    x = 0.5 * (2 * c + a) / total
    y = (np.sqrt(3) / 2) * a / total
    return x, y

# Triangle vertices
A_vertex = (0.5, np.sqrt(3)/2)
B_vertex = (0, 0)
C_vertex = (1, 0)

# Arbitrary phase boundary lines (example: not triangles)
phase_alpha = [
    (0.0, 0.0), 
    (0.18, 0.0), 
    (0.32, 0.22), 
    (0.36, 0.28), 
    (0.44, 0.34), 
    (0.5, 0.36), 
    (0.5, np.sqrt(3)/2), 
    (0.0, 0.0)
]
phase_beta = [
    (0.18, 0.0),
    (1.0, 0.0),
    (0.5, np.sqrt(3)/2),
    (0.5, 0.36),
    (0.44, 0.34),
    (0.36, 0.28),
    (0.32, 0.22),
    (0.18, 0.0)
]
phase_gamma = [
    (0.0, 0.0),
    (0.18, 0.0),
    (0.32, 0.22),
    (0.36, 0.28),
    (0.44, 0.34),
    (0.5, 0.36),
    (1.0, 0.0),
    (0.0, 0.0)
]

phase_regions = {
    "α": phase_alpha,
    "
