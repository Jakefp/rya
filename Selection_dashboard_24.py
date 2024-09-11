import streamlit as st
import pandas as pd
import openpyxl
import plotly.graph_objects as go
from functions import *
import hmac

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False
    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True
    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False
if not check_password():
    st.stop()  # Do not continue if check_password is not True.


##### Main

st.set_page_config(layout="wide")
####################################
Classes = [
    '420',
    'ILCA 7',
    'ILCA 6 Male',
    'ILCA 6 Female',
    'IQFoil Male', 
    'IQFoil Female',
    'Kite Male',
    'Kite Female'
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
if selected_class == "ILCA 6 Male":
    st.write("Note: Sailors that completed indicator result in a junior class:")
    st.write("Toby Wagget, Oscar Bartlett, Ben Anderson, Tate Kump, William Brown, Corneille Leprince, Max Guiguet-Belcher")
elif selected_class == "IQFoil Male":
    st.write("Note: Sailors that completed indicator result in a junior class:")
    st.write("Oliver Ebdon, George Ebdon, Finley Christopher-Knight, Milo Shaw, Ned Bentley-Taylor")
elif selected_class == "IQFoil Female":
    st.write("Note: Sailors that completed indicator result in a junior class:")
    st.write("Sophie Clark, Evelyn Clark, Rebecca Pilkington")
elif selected_class == "420":
    st.header("Note sailors that are part of a Mixed team:")
    st.write("Male: Helm: Joseph Jones. Crew: Charlie Howard, George Self, Naythan Twiggs")
    st.write("Female: Helm: Laragh Epstein, Ella Martin, Nia Mecklenburgh, Jessica Skelding. Crew: Hennie Burlton.")
### Currently working here!!!!!!!!
create_scatter_chart_class(data)

st.divider()
if selected_class == "420":
    st.header("Potential and Performance Ranking")
    selected_columns = ['Name','Helm/Crew', 'Potential Ranking', 'Performance Ranking', 'Potential and Performance']
    filtered_data = data[selected_columns]
    sorted_data = filtered_data.sort_values(by='Potential and Performance')
    st.dataframe(sorted_data,hide_index=True)
else:
    # Create two columns with titles "Performance" and "Potential"
    col1, col2 = st.columns(2)

    with col1:
        st.header("Potential")
        st.write("Potential Ranking")
        selected_columns = ['Name', 'Potential Ranking', 'Potential Score']
        filtered_data = data[selected_columns]
        sorted_data = filtered_data.sort_values(by='Potential Ranking')
        st.dataframe(sorted_data,hide_index=True)
        create_radar_chart_class(data)

    with col2:
        st.header("Performance")
        st.write("Performance Ranking")
        selected_columns = ['Name', 'Performance Ranking', 'Performance Score']
        filtered_data = data[selected_columns]
        sorted_data = filtered_data.sort_values(by='Performance Ranking')
        st.dataframe(sorted_data,hide_index=True)
        create_bar_chart_class(data)

st.divider()
st.header("Athlete Height compared to Class Reccomendations")
st.write("Below red line = Performance Limiting")
st.write("Between red and green line = Performance Foundation")
st.write("Above green line = Performance Defining")

#st.markdown("<span style='color:green'>Performance Defining</span>", unsafe_allow_html=True)
#st.markdown("<span style='color:orange'>Performance Foundation</span>", unsafe_allow_html=True)
#st.markdown("<span style='color:red'>Performance Limiting</span>", unsafe_allow_html=True)

if selected_class == "420":
    # Filter data where the "Helm/Crew" column has the value "Helm"
    data_helm = data[data['Helm/Crew'] == "Helm"]

    # Display the Helm heights
    st.header("Helm Heights:")
    create_height_bar_chart(data_helm, height_data, "470 mixed helm")

    # Filter data where the "Helm/Crew" column has the value "Crew" (if needed for crew heights)
    data_crew = data[data['Helm/Crew'] == "Crew"]

    # Display the Crew heights
    st.header("Crew Heights:")
    create_height_bar_chart(data_crew, height_data, "470 mixed crew")
else:
    # For other classes, display the data as it is
    create_height_bar_chart(data, height_data, selected_class)

st.divider()

st.write(f'## Specific Athlete Deep Dive' )
selected_athlete = st.selectbox("Select Athlete", data["Name"])
# st.header("Athlete profiles currently being generated")
st.image(f"athlete_profiles/{selected_class}/{selected_athlete}.jpg")
# st.image(f"{selected_class}/{selected_athlete}.png")
# st.write("Values and Behaviours Breakdown")
# st.image(f"{selected_class}/{selected_athlete}VB.png")
# st.write("Brilliant Racer Breakdown")
# st.image(f"{selected_class}/{selected_athlete}BR.png")


st.write("Data visuals: Jake Farren-Price")

# pw: LA2028!

#Notes: Performance number and Potential 
