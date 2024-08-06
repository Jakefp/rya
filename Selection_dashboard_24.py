import hmac
import streamlit as st
import pandas as pd
import openpyxl

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

file_path = 'CoachSailorReviewFormSelection_Cognito export.xlsx'
excel_data = pd.read_excel(file_path, engine='openpyxl')

# Title of the app
st.title('Youth 2024 Selections')

# Dropdown to select class
Classes = excel_data['Class being reviewed'].unique().tolist()
selected_class = st.sidebar.selectbox("Select Class", Classes)
#Function for getting the name and class of sailors
Athlete_class_specific = excel_data[excel_data['Class being reviewed'] == selected_class]
    
# Dropdown to select athlete within the selected class
Athlete_names = Athlete_class_specific['Sailor being reviewed (Name or Bib number)'].tolist()
selected_athlete = st.sidebar.radio("Select Athlete", Athlete_names)

# Write something generic above the columns
st.write("Here you can analyse the performance and potential of various candidates for the Youth 2024 selections.")

st.write("## Overall Class Performance vs Potential")

st.write(f'{selected_athlete}')

create_radar_chart(excel_data,selected_athlete)
#create_radar_chart_class(excel_data, selected_class)

st.divider()

# Create two columns with titles "Performance" and "Potential"
col1, col2 = st.columns(2)

with col1:
    st.header("Performance")
    st.write(f"Performance data for {selected_athlete}")
    # Add content for the Performance column

with col2:
    st.header("Potential")
    st.write(f"Performance data for {selected_athlete}")
    # Add content for the Potential column

# You can then add logic to update the content based on the button selected

for i, class_name in enumerate(Classes):
    if Athlete_names == class_name:
        with col1:
            st.write(f"Performance data for {class_name}")
        with col2:
            st.write(f"Potential data for {class_name}")
        break

# file_path = 'CoachSailorReviewFormSelection_Cognito export.xlsx'
# excel_data = pd.read_excel(file_path, engine='openpyxl')

# # Title of the app
# st.title('Youth 2024 Selections')

# #Youth Classes
# # Classes = ('ILCA 6 Male', 'ILCA 6 Female', 'Nacra 15', '29er Female', '29er Male/Mix', 'IQFoil Female', 'IQFoil Male', 'KiteFoil Female', 'KiteFoil Male', '420 Female', '420 Male/Mixed')
# # Athletes = excel_data.iloc[:,1]

# # Dropdown to select class
# Classes = excel_data['Class being reviewed'].unique().tolist()
# selected_class = st.sidebar.selectbox("Select Class", Classes)
# #Function for getting the name and class of sailors
# Athlete_class_specific = excel_data[excel_data['Class being reviewed'] == selected_class]
    
# # Dropdown to select athlete within the selected class
# Athlete_names = Athlete_class_specific['Sailor being reviewed (Name or Bib number)'].tolist()
# selected_athlete = st.sidebar.radio("Select Athlete", Athlete_names)

# # Write something generic above the columns
# st.write("Here you can analyse the performance and potential of various candidates for the Youth 2024 selections.")

# st.write("## Overall Class Performance vs Potential")

# st.divider()

# # Create two columns with titles "Performance" and "Potential"
# col1, col2 = st.columns(2)

# with col1:
#     st.header("Performance")
#     st.write(f"Performance data for {selected_athlete}")
#     # Add content for the Performance column

# with col2:
#     st.header("Potential")
#     st.write(f"Performance data for {selected_athlete}")
#     # Add content for the Potential column

# # You can then add logic to update the content based on the button selected

# for i, class_name in enumerate(Classes):
#     if Athlete_names == class_name:
#         with col1:
#             st.write(f"Performance data for {class_name}")
#         with col2:
#             st.write(f"Potential data for {class_name}")
#         break


#     #notes from your queen: I think the dropdown should be for 
#     #selecting the class, and the buttons should be for selecting
#     #the athletes, so you can show multiple athletes at once and 
#     #compare them directly
