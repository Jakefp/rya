import streamlit as st
import pandas as pd
import openpyxl
import plotly.graph_objects as go
from functions import *

##### Main

st.set_page_config(layout="wide")
####################################
Classes = [
    'ILCA 7',
    'ILCA 6 Male',
    'ILCA 6 Female',
    'IQ Foil Male'
    # Add other classes and sheet names here
]
st.image("bys.png", width=300)
st.title('Youth 2024 Selections')

st.write("Here you can analyse the performance and potential of various candidates for the Youth 2024 selections.")
selected_class = st.selectbox("Select Youth Class", Classes)
data = pd.read_excel('master.xlsx', engine='openpyxl', sheet_name=selected_class)
st.write("## Class Performance vs Potential")
height_data = pd.read_excel('master.xlsx', engine='openpyxl', sheet_name="Heights")

st.image("Performance_Potential.png")

create_scatter_chart_class(data)

st.divider()

# Create two columns with titles "Performance" and "Potential"
col1, col2 = st.columns(2)

with col1:
    st.header("Potential")
    st.write("Potential Ranking")
    selected_columns = ['Name', 'Potential Ranking', 'Potential Score']
    filtered_data = data[selected_columns]
    st.dataframe(filtered_data)
    create_radar_chart_class(data)

with col2:
    st.header("Performance")
    st.write("Performance Ranking")
    selected_columns = ['Name', 'Performance Ranking', 'Performance Score']
    filtered_data = data[selected_columns]
    st.dataframe(filtered_data)
    create_bar_chart_class(data)

st.divider()
st.header("Athlete Height compared to Class Reccomendations")
st.write("Below red line = Performance Limiting")
st.write("Between red and green line = Performance Foundation")
st.write("Above green line = Performance Defining")

#st.markdown("<span style='color:green'>Performance Defining</span>", unsafe_allow_html=True)
#st.markdown("<span style='color:orange'>Performance Foundation</span>", unsafe_allow_html=True)
#st.markdown("<span style='color:red'>Performance Limiting</span>", unsafe_allow_html=True)

create_height_bar_chart(data, height_data, selected_class)

st.divider()

st.write(f'## Specific Athlete Deep Dive' )
selected_athlete = st.selectbox("Select Athlete", data["Name"])
st.image(f"athlete_profiles/{selected_class}/{selected_athlete}.jpeg")

st.write("Data visuals: Jake Farren-Price")

# pw: athlete#tree#table

#Notes: Performance number and Potential 
