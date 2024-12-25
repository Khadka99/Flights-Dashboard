import streamlit as st
import pandas as pd
from dbhelper import DB
import plotly.graph_objects as go
import plotly.express as px

db = DB()

st.sidebar.title('Flights Analytics')

user_option = st.sidebar.selectbox('Menu',['OverView','Check Flights','Check Average Price','Analytics'])

if user_option == 'Check Flights':
    st.title('Check Flights')

    col1,col2 = st.columns(2)

    city = db.fetch_city_names()

    with col1:
        source = st.selectbox('Source',sorted(city))
    with col2:
        destination = st.selectbox('Destination', sorted(city))

    if st.button('Search'):
        results = db.fetch_all_flights(source,destination)
        # Define column names
        columns = ["Airline", "Route", "Dep_Time", "Duration", "Price"]

        # Convert result to DataFrame
        if results:
            df = pd.DataFrame(results, columns=columns)
            st.dataframe(df)  # Display DataFrame with column names
        else:
            st.write("No flights found for the selected Source and Destination.")

        #st.dataframe(results)

elif user_option == "Check Average Price":
    st.title("Average Price For Airline Vs Destination")
    result = db.avg_price_per_airlines()

    # columns = ["Source","Destination","Airline","Avg_Price","Rank"]
    # df = pd.DataFrame(result,columns=columns)
    st.dataframe(result)

elif user_option == 'Analytics':
    airline, frequency = db.fetch_airline_frequency()
    fig = go.Figure(
        go.Pie(
            labels=airline,
            values=frequency,
            hoverinfo="label+percent",
            textinfo="value"
        ))

    st.subheader("Number of Flights Per Airlines")
    st.plotly_chart(fig)

    city, frequency = db.busy_airport()
    colors = ['blue', 'green', 'orange', 'red', 'purple', 'pink', 'yellow', 'teal']
    fig = go.Figure(
        go.Bar(
            x=city,
            y=frequency,
            text=frequency,
            textposition='auto',
            marker=dict(color=colors),
            textfont=dict(  # Customize data label font
                color="black",  # Font color for data labels
                size=14,  # Font size for data labels
                family="Arial"  # Font family for data labels
            ),
            hoverinfo="x+y"))

    st.subheader("Busy Airport")
    st.plotly_chart(fig)

    date,frequency = db.daily_frequency()

    # Custom colors for line and markers
    line_color = "blue"
    marker_color = "red"

    # Create the line chart
    fig = go.Figure(
        go.Scatter(
            x=date,  # X-axis categories
            y=frequency,  # Y-axis values
            mode='lines+markers+text',  # Display lines, markers, and text labels
            text=frequency,  # Data labels
            textposition='top center',  # Position data labels above the markers
            line=dict(color=line_color, width=1),  # Line color and width
            marker=dict(
                color=marker_color,  # Marker color
                size=10  # Marker size
            ),
            hoverinfo="x+y"  # Display city and frequency on hover
        )
    )

    # Add a header and render the chart in Streamlit
    st.subheader("Daily Flights")
    st.plotly_chart(fig)


    time, frequency, price = db.dep_time_and_price()

    # Custom colors for line and markers
    line_color = "green"
    marker_color = "red"

    # Create the line chart
    fig = go.Figure(
        go.Scatter(
            x=time,  # X-axis categories
            y=price,  # Y-axis values
            mode='lines+markers+text',  # Display lines, markers, and text labels
            text=frequency,  # Data labels
            textposition='top center',  # Position data labels above the markers
            line=dict(color=line_color, width=2),  # Line color and width
            marker=dict(
                color=marker_color,  # Marker color
                size=10  # Marker size
            ),
            hoverinfo="x+y"  # Display city and frequency on hover
        )
    )
    st.subheader("Time Vs Price")
    st.plotly_chart(fig)


else:
    st.title("Flight Data Analysis Dashboard")

    # Add a brief description
    st.markdown("""
        ### Welcome to the Flight Data Analysis Dashboard!

        This project provides a comprehensive analysis of flight details, helping users gain valuable insights into flight patterns, pricing trends, and travel dynamics. The dataset includes crucial flight information such as:

        - **Airline**: The carrier operating the flight.
        - **Date of Journey**: The travel date, offering insights into seasonality and trends.
        - **Source and Destination**: The cities of departure and arrival.
        - **Route**: The flight path, including layovers.
        - **Departure Time**: The time the flight departs, categorized into time slots like morning, afternoon, and evening.
        - **Duration**: The total travel time.
        - **Total Stops**: The number of layovers during the journey.
        - **Price**: The ticket cost, enabling pricing pattern analysis.

        ---

        #### **Dashboard Features**
        1. **Interactive Visualizations**: Analyze flight data through bar charts, line graphs, scatter plots, and more.
        2. **Price Trends**: Explore how ticket prices vary based on factors like time of journey, airlines, and stops.
        3. **Travel Patterns**: Identify peak travel times and popular routes.
        4. **Duration Analysis**: Compare travel times across airlines and routes to find the most efficient flights.
        5. **Filter and Search**: Customize your analysis by selecting specific airlines, travel dates, or destinations.

        ---

        #### **Objective**
        This project aims to provide users with actionable insights to make informed decisions about flight bookings and understand market trends in the aviation industry.

        Explore the data and uncover patterns that impact travel choices!
        """)

    # Add a footer or tagline
    st.markdown("**Get started by selecting a Analytics or Check Flights!**")
