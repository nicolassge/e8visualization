import streamlit as st
import pandas as pd
import plotly.express as px
# Set up the Streamlit page layout
st.set_page_config(layout="wide")

# Load dataset
airbnb_data = pd.read_csv("airbnb.csv")

# Dashboard title
st.title("Nicolas Gonzalez")

# Create navigation tabs
data_tab, analysis_tab, simulator_tab = st.tabs(["Explore Data", "In-Depth Insights", "Price Estimator"])
# ====== TAB 1: Explore Data ======
with data_tab:
    st.header("Explore AIRBNBs in Madrid")

    # Sidebar filters
    st.sidebar.header("Filters")
    area_groups = st.sidebar.multiselect("Choose a Neighborhood Group", airbnb_data["neighbourhood_group"].unique(), default=airbnb_data["neighbourhood_group"].unique())
    area = st.sidebar.multiselect("Choose a Neighborhood", airbnb_data["neighbourhood"].unique(), default=airbnb_data["neighbourhood"].unique())
    accommodation_type = st.sidebar.multiselect("Choose Room Type", airbnb_data["room_type"].unique(), default=airbnb_data["room_type"].unique())

    # Apply filters
    filtered_data = airbnb_data[
        (airbnb_data["neighbourhood_group"].isin(area_groups)) &
        (airbnb_data["neighbourhood"].isin(area)) &
        (airbnb_data["room_type"].isin(accommodation_type))
    ]

    # Visualization: Room type vs. Reviews
    st.subheader("ROOM TYPES vs. REVIEWS")
    review_chart = px.bar(filtered_data, x="room_type", y="number_of_reviews", color="room_type", title="Review Count by Room Type")
    st.plotly_chart(review_chart)

    # Visualization: Price distribution
    st.subheader("Room Type Price Distribution")
    price_chart = px.box(filtered_data, x="room_type", y="price", title="Room Type Pricing")
    st.plotly_chart(price_chart)

    # ====== TAB 2: In-Depth Insights ======
with analysis_tab:
    st.header("Advanced Airbnb Analysis")
    
    column1, column2 = st.columns(2)

    with column1:
        st.subheader("Map of Listings")
        st.map(filtered_data.dropna(), latitude="latitude", longitude="longitude")
    
    with column2:
        st.subheader("Neighborhood Price Distribution")
        price_boxplot = px.box(filtered_data[filtered_data["price"] < 600], x="neighbourhood", y="price", title="Price Ranges Across Neighborhoods")
        st.plotly_chart(price_boxplot)
    
    # Top 10 Hosts
    st.subheader("Top 10 Hosts by Listings")
    host_summary = filtered_data.groupby(["host_id", "host_name"]).size().reset_index()
    host_summary["host"] = host_summary["host_id"].astype(str) + " --- " + host_summary["host_name"]
    top_hosts = host_summary.sort_values(by=0, ascending=False).head(10)
    host_chart = px.bar(top_hosts, x=0, y="host", orientation='h', title="Hosts with Most Listings")
    st.plotly_chart(host_chart)

    # ====== TAB 3: Price Estimator ======
with simulator_tab:
    st.header("Airbnb Price Estimator")

    # User selections
    chosen_neighborhood = st.selectbox("Pick a Neighborhood", airbnb_data["neighbourhood"].unique())
    chosen_room = st.selectbox("Pick a Room Type", airbnb_data["room_type"].unique())
    stay_duration = st.number_input("Number of Nights", min_value=1, value=1)

    # Filter for selected options
    similar_listings = airbnb_data[(airbnb_data["neighbourhood"] == chosen_neighborhood) & (airbnb_data["room_type"] == chosen_room)]

    if not similar_listings.empty:
        avg_night_price = similar_listings["price"].mean()
        min_night_price = similar_listings["price"].min()
        max_night_price = similar_listings["price"].max()

        st.subheader("Suggested Price Range")
        st.write(f"💰 **Average price per night:** {avg_night_price:.2f} €")
        st.write(f"📉 **Minimum price per night:** {min_night_price:.2f} €")
        st.write(f"📈 **Maximum price per night:** {max_night_price:.2f} €")
        st.write(f"🔢 **Total cost for {stay_duration} nights:** {avg_night_price * stay_duration:.2f} €")
    else:
        st.write("No data available for the selected neighborhood and room type.")
        

       