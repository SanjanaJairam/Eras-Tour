# app.py
import streamlit as st
from data_processing import load_data, preprocess_data
from charts import (
    plot_frequency_heatmap, plot_live_songs_bar, plot_song_order_swarm,
    plot_musicality_eras_concert, plot_compare_musicality_cities,
    plot_popularity_vs_occurrences, plot_popularity_recorded_songs,
    plot_tickets_sold_across_cities
)
import pandas as pd

def main():
    # Load data
    df, venue_df, all_songs = load_data()

    # Preprocess data
    cleaned_df, metrics_change_df = preprocess_data(df, venue_df)

    # Define Colors for Eras
    era_color_mapping = {
        'Intro': '#c6e597',
        'Taylor swift (debut)': 'teal',
        'Fearless': 'gold',
        'Speak now': 'indigo',
        'Red': 'firebrick',
        '1989': 'lightblue',
        'Reputation': '#232b2b',
        'Lover': 'deeppink',
        'Folklore': 'grey',
        'Evermore': 'tan',
        'Midnights': 'navy',
        'Surprise Songs': 'white',
        'Music video premiere': 'orange'
    }

    # Streamlit app code
    st.sidebar.header("Navigation")
    selected_chart = st.sidebar.radio("Select Chart", [
        "Frequency of songs played", "Number of Songs performed live",
        "Song Order by Era", "Musicality for Eras Concert",
        "Compare Musicality: Cities", "Popularity vs. Song Occurrences",
        "Popularity of Recorded Songs by Album", "Tickets Sold across cities"
    ])

    # Interactive Elements
    selected_era = st.sidebar.selectbox("Select Era", ['All'] + list(era_color_mapping.keys()))
    selected_city1 = st.sidebar.selectbox("Select City 1", ['All'] + list(cleaned_df['city'].unique()))
    selected_city2 = st.sidebar.selectbox("Select City 2", ['All'] + list(cleaned_df['city'].unique()))

    st.image('ts_data/eras-tour.jpg')
    
    # Filter Data based on Interactive Elements
    filtered_df = cleaned_df.copy()

    # Filter based on era
    if selected_era != 'All':
        filtered_df = filtered_df[filtered_df['era_name'] == selected_era]

    # Filter based on city
    if selected_city1 != 'All':
        filtered_df_city1 = filtered_df[filtered_df['city'] == selected_city1]

        # If a second city is selected, filter again
        if selected_city2 != 'All':
            filtered_df_city2 = filtered_df[filtered_df['city'] == selected_city2]
            filtered_df = pd.concat([filtered_df_city1, filtered_df_city2])

        # If only one city is selected, use the filtered_df_city1
        else:
            filtered_df = filtered_df_city1


    if selected_chart == "Frequency of songs played":
        plot_frequency_heatmap(filtered_df, era_color_mapping)

    elif selected_chart == "Number of Songs performed live":
        era_counts = filtered_df['era_name'].value_counts().reset_index()
        era_counts.columns = ['era_name', 'count']
        plot_live_songs_bar(era_counts, era_color_mapping)

    elif selected_chart == "Song Order by Era":
        plot_song_order_swarm(filtered_df, era_color_mapping)

    elif selected_chart == "Musicality for Eras Concert":
        plot_musicality_eras_concert(metrics_change_df)

    elif selected_chart == "Compare Musicality: Cities":
        plot_compare_musicality_cities(filtered_df, selected_city1, selected_city2)

    elif selected_chart == "Popularity vs. Song Occurrences":
        song_occurrences = filtered_df.groupby(['song_name', 'id', 'era_name', 'popularity']).agg({'song_order': 'count'}).reset_index()
        song_occurrences = song_occurrences.rename(columns={'song_order': 'count'})
        song_occurrences = song_occurrences.sort_values(by=['count'], ascending=False)
        plot_popularity_vs_occurrences(song_occurrences, era_color_mapping)

    elif selected_chart == "Popularity of Recorded Songs by Album":
        recorded_songs_popularity = all_songs[['song_name', 'album', 'id', 'popularity']]
        recorded_songs_popularity['performed_live'] = recorded_songs_popularity['id'].isin(cleaned_df['id'].unique())
        recorded_songs_popularity['performed_live'] = recorded_songs_popularity['performed_live'].astype(bool)
        plot_popularity_recorded_songs(recorded_songs_popularity)

    elif selected_chart == "Tickets Sold across cities":
        venue_capacity = {
            'Glendale': 78600, 'Las Vegas': 71835, 'Arlington': 105000, 'Tampa': 75000, 'Houston': 80000,
            'Atlanta': 75000, 'Nashville': 69143, 'Philadelphia': 69896, 'Foxborough': 65878,
            'East Rutherford': 88491, 'Chicago': 61500, 'Detroit': 78000, 'Pittsburgh': 75000,
            'Minneapolis': 73000, 'Cincinnati': 65515, 'Kansas City': 76416, 'Denver': 84000,
            'Seattle': 72000, 'Santa Clara': 68500, 'Los Angeles': 100240, 'Inglewood': 70240, 'Mexico City': 65000
        }
        venue_df['capacity'] = venue_df['city'].map(venue_capacity)
        plot_tickets_sold_across_cities(venue_df)
    # Add similar conditions for other charts...

if __name__ == "__main__":
    main()
