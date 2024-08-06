
import streamlit as st
import plotly.graph_objects as go

### First Character

def first_char(cell_value):
    try:
        return int(str(cell_value)[0])
    except ValueError:
        return 0  # Default value if conversion fails

### Wrapping titles on graphs
# def wrap_text(text, width):
#     return '\n'.join([text[i:i+width] for i in range(0, len(text), width)])


### Radar Chart - single athlete

def create_radar_chart(excel_data, athlete_name):

    athlete_row = excel_data[excel_data['Sailor being reviewed (Name or Bib number)'] == athlete_name]
    #I need to add in averaging for each sailor and then move onto putting the whole class on one graph

    categories = [
        'Sailor is fast in all conditions',
        'Sailor is\xa0a Mentally Robust Athlete',
        'Sailor is\xa0a Physically Robust Athlete',
        'Sailor is\xa0an excellent non-dependent decision maker',
        'Sailor\xa0can excel under the most extreme pressure'
    ]

    # Extract the scores for the selected categories
    values = [
        first_char(athlete_row[categories[0]].values[0]),
        first_char(athlete_row[categories[1]].values[0]),
        first_char(athlete_row[categories[2]].values[0]),
        first_char(athlete_row[categories[3]].values[0]),
        first_char(athlete_row[categories[4]].values[0])
    ]
 
    # Ensure the radar chart is circular by repeating the first value
    
    values += values[:1]
    categories += categories[:1]

    #wrapped_categories = [wrap_text(category, 20) for category in categories]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=athlete_name
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickvals=[1, 2, 3, 4, 5],
                ticktext=["1", "2", "3", "4", "5"]
            ),
        ),
        title=f"Performance Metrics: {athlete_name}",
        showlegend=False
    )

    st.plotly_chart(fig)

    return

### Radar Chart - class

def create_radar_chart_class(excel_data, selected_class):

    categories = [
        'Sailor is fast in all conditions',
        'Sailor is\xa0a Mentally Robust Athlete',
        'Sailor is\xa0a Physically Robust Athlete',
        'Sailor is\xa0an excellent non-dependent decision maker',
        'Sailor\xa0can excel under the most extreme pressure'
    ]

    fig = go.Figure()
    #Need this to return a dataframe with all the athletes that are in this class - getting index 0 error again
    for athlete_name in selected_class:
        athlete_row = excel_data[excel_data['Sailor being reviewed (Name or Bib number)'] == athlete_name]

        # Extract the scores for the selected categories
        values = [
            first_char(athlete_row[categories[0]].values[0]),
            first_char(athlete_row[categories[1]].values[0]),
            first_char(athlete_row[categories[2]].values[0]),
            first_char(athlete_row[categories[3]].values[0]),
            first_char(athlete_row[categories[4]].values[0])
        ]
        
        # Ensure the radar chart is circular by repeating the first value
        values += values[:1]

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=athlete_name
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickvals=[1, 2, 3, 4, 5],
                ticktext=["1", "2", "3", "4", "5"]
            ),
        ),
        title="Performance Metrics",
        showlegend=True
    )

    st.plotly_chart(fig)