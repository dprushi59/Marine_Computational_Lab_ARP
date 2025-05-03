import streamlit as st
st.set_page_config(page_title="Shear Force and Bending Moment Visualization", layout="wide")

import numpy as np
import matplotlib.pyplot as plt
import os
from calculations import calculate_shear_force_and_bending_moment
from data import calculateResults
from plots import (
    plot_shear_force_by_section,
    plot_shear_force_by_time,
    plot_bending_moment_by_section,
    plot_bending_moment_by_time,
)

# Title
st.title("Shear Force and Bending Moment Visualization")

# Input parameters for calculateResults
st.header("Ship Parameters")
lamdaByL = st.number_input("λ / L:", value=1.2, step=0.01)
length = st.number_input("Length (m):", value=122.1, step=0.1)
draft = st.number_input("Draft (m):", value=7.8, step=0.1)
displacement = st.number_input("Displacement (tons):", value=14000, step=100)
bml = st.number_input("BML (m):", value=128.1, step=0.1)

# Upload .txt file
st.header("Upload Input File")
uploaded_file = st.file_uploader("Upload a .txt input file", type=["txt"])

# Time settings
st.header("Time Settings")
t_min = st.number_input("Start time t_min (s):", value=0)
t_max = st.number_input("End time t_max (s):", value=10)
num_points = st.number_input("Number of time points:", value=100, min_value=10)

# Generate time array
t = np.linspace(t_min, t_max, num_points)

# If file is uploaded
if uploaded_file:
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", "in.txt")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File saved to: {file_path}")

    # Calculate output parameters from ship inputs
    output_data = calculateResults(lamdaByL, length, draft, displacement, bml)

    # Perform shear force and bending moment calculation
    shear_force, bending_moment = calculate_shear_force_and_bending_moment(
        output_data['a33'], output_data['b33'], output_data['c33'],
        output_data['a55'], output_data['b55'], output_data['c55'],
        output_data['omega'], output_data['Awl'], displacement,
        output_data['I55'], bml, output_data['section_positions'], t
    )

    section_positions = output_data['section_positions']
    section_positions_array = np.array(section_positions)
    st.header("Shear Force Plots")

    x_val_shear = st.slider("Select section position for shear force (m):",
                            min_value=float(section_positions[0]),
                            max_value=float(section_positions[-1]),
                            value=float(section_positions[0]))
    fig, ax = plt.subplots()
    plot_shear_force_by_section(x_val_shear, section_positions_array, shear_force, t, ax)
    st.pyplot(fig)

    t_val_shear = st.slider("Select time for shear force (s):",
                            min_value=float(t[0]), max_value=float(t[-1]), value=float(t[0]))
    fig, ax = plt.subplots()
    plot_shear_force_by_time(t_val_shear, t, section_positions_array, shear_force, ax)
    st.pyplot(fig)

    st.header("Bending Moment Plots")

    x_val_bending = st.slider("Select section position for bending moment (m):",
                              min_value=float(section_positions[0]),
                              max_value=float(section_positions[-1]),
                              value=float(section_positions[0]))
    fig, ax = plt.subplots()
    plot_bending_moment_by_section(x_val_bending, section_positions_array, bending_moment, t, ax)
    st.pyplot(fig)

    t_val_bending = st.slider("Select time for bending moment (s):",
                              min_value=float(t[0]), max_value=float(t[-1]), value=float(t[0]))
    fig, ax = plt.subplots()
    plot_bending_moment_by_time(t_val_bending, t, section_positions_array, bending_moment, ax)
    st.pyplot(fig)

else:
    st.warning("Please upload a `.txt` file to begin calculations.")
