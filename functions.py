
import streamlit as st
import plotly.graph_objects as go
import numpy
import random

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
def create_radar_chart_class(data):

    athlete_names = data['Name'].unique()

    categories = [
        'Values and Behaviours: Score',
        'Medal Winning Strength: Score',
        'Performance and Execution Under Pressure: Score',
        'Brilliant Racer: Score',
        'Physical Score'
    ]

    fig = go.Figure()
    for athlete_name in athlete_names:
        athlete_row = data[data['Name'] == athlete_name]

        # Extract the scores for the selected categories
        values = [
            athlete_row[categories[0]].values[0],
            athlete_row[categories[1]].values[0],
            athlete_row[categories[2]].values[0],
            athlete_row[categories[3]].values[0],
            athlete_row[categories[4]].values[0]
        ]
        
        # Ensure the radar chart is circular by repeating the first value
        values += values[:1]
        categories += categories[:1]

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
                tickvals=[1, 2, 3, 4],
                ticktext=["1", "2", "3", "4"]
            ),
        ),
        # title="Potential Metrics",
        showlegend=True
    )

    st.plotly_chart(fig)

### Bar Chart Performance for Class
def create_bar_chart_class(data):

    athlete_names = data['Name'].unique()
    indicator = data['Indicator Result']
    six_month = data['6 Month Result'] 

    data = data.sort_values(by='Indicator Result', ascending=True)

    fig = go.Figure()

    # Add the first set of bars for the Indicator Result
    fig.add_trace(go.Bar(
        y=athlete_names,  # Y-axis will be the athlete names
        x=indicator,  # X-axis will be the indicator result
        name='Indicator Result',
        orientation='h',  # Horizontal bars
        marker=dict(color='dark blue')  # Color for the bars
    ))

    # Add the second set of bars for the 6 Month Result
    fig.add_trace(go.Bar(
        y=athlete_names,  # Y-axis will be the athlete names
        x=six_month,  # X-axis will be the six-month result
        name='6 Month Result',
        orientation='h',  # Horizontal bars
        marker=dict(color='light blue')  # Color for the bars
    ))

    fig.update_layout(
        barmode='stack',
        title="*Athletes with no 6 Month Ranking have no second bar",
        yaxis_title="Athletes",  # Swap x and y
        xaxis_title="Scores",  # Swap x and y
        xaxis=dict(showgrid=True, gridcolor='LightGray'),  # Enable x-axis grid lines
        yaxis=dict(showgrid=True, gridcolor='LightGray'),  # Enable y-axis grid lines
        yaxis_autorange='reversed',
        showlegend=True
    )

    st.plotly_chart(fig)


### Scatter Performance vs Potential
def create_scatter_chart_class(data):

    athlete_names = data['Name'].unique()
    performance = data['Performance Score']
    potential = data['Potential Score']

    colors = [f'#{random.randint(0, 0xFFFFFF):06x}' for _ in athlete_names]

    fig = go.Figure()

    # Add each athlete's data as a separate trace to include them in the legend
    for i, athlete in enumerate(athlete_names):
        athlete_data = data[data['Name'] == athlete]
        fig.add_trace(go.Scatter(
            x=athlete_data['Performance Score'],
            y=athlete_data['Potential Score'],
            mode='markers',
            text=athlete,  # Show athlete's name on hover
            marker=dict(
                size=20,
                color=colors[i],  # Assign a unique color to each athlete
                opacity=0.8
            ),
            name=athlete  # This will add the athlete's name to the legend
        ))

    fig.update_layout(
        # title="Performance vs Potential",
        xaxis_title="Performance",
        yaxis_title="Potential",
        xaxis=dict(showgrid=True, gridcolor='LightGray', autorange='reversed'),
        yaxis=dict(showgrid=True, gridcolor='LightGray'),
        showlegend=True,
        autosize=True,  # Disable autosize to manually control the size
        # width=600,  # Set the width of the plot
        # height=600,  # Set the height of the plot equal to the width
        # margin=dict(l=50, r=50, b=50, t=50),  # Set the margins
    )

    st.plotly_chart(fig)

### Bar chart for heights and predicted height
def create_height_bar_chart(data,height_data,selected_class):

    selected_row = height_data.loc[height_data['Class'] == selected_class]

    # Extract the relevant height values
    performance_limiting = selected_row['Performance Limiting'].values[0]
    performance_foundation = selected_row['Performance Foundation'].values[0]
    performance_defining = selected_row['Performance Defining'].values[0]

    # Now you can pass these values to your function or use them as needed
    height_data_dict = {
        "Performance Limiting": performance_limiting,
        "Performance Foundation": performance_foundation,
        "Performance Defining": performance_defining
    }
    athlete_names = data['Name'].unique()
    actual = data['Height']
    predicted = data['Predicted Height'] 

    data = data.sort_values(by='Height', ascending=False)

    fig = go.Figure()

    # Add the first set of bars for the Indicator Result
    fig.add_trace(go.Bar(
        x=athlete_names,  # Y-axis will be the athlete names
        y=actual,  # X-axis will be the indicator result
        name='Current Height',
        orientation='v',  # Horizontal bars
        marker=dict(color='dark blue')  # Color for the bars
    ))

    # Add the second set of bars for the 6 Month Result
    fig.add_trace(go.Bar(
        x=athlete_names,  # Y-axis will be the athlete names
        y=predicted,  # X-axis will be the six-month result
        name='Predicted Height',
        orientation='v',  # Horizontal bars
        marker=dict(color='light blue')  # Color for the bars
    ))

    # Adding horizontal lines for required heights
    for label, height in height_data_dict.items():
        color = "red" if label == "Performance Limiting" else "orange" if label == "Performance Foundation" else "green"
        fig.add_shape(
            type="line",
            x0=-0.5,  # Start of the line on the x-axis
            y0=height,
            x1=len(athlete_names)-0.5,  # End of the line on the x-axis
            y1=height,
            line=dict(
                color=color,
                width=2,
                dash="dash"
            ),
            name=label
        )
        fig.add_annotation(
            x=len(athlete_names)-0.5,  # Place the label at the end of the line
            y=height,
            text=f'{label} ({height} cm)',
            showarrow=False,
            yshift=10
        )

    fig.update_layout(
        #barmode='stack',
        #title="Athlete Height compared to Class Reccomendations",
        yaxis_title="Heights",  # Swap x and y
        xaxis_title="Athletes",  # Swap x and y
        xaxis=dict(showgrid=True, gridcolor='LightGray'),  # Enable x-axis grid lines
        yaxis=dict(showgrid=True, gridcolor='LightGray', range=[100,200]),  # Enable y-axis grid lines
        #yaxis_autorange='reversed',
        showlegend=True
    )

    st.plotly_chart(fig)