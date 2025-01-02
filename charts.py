# charts.py
import streamlit as st
import plotly.subplots as sub_plt
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import pydeck as pdk
from matplotlib.lines import Line2D
import pandas as pd

metrics = [
    'acousticness',
    'danceability',
    'energy',
    'instrumentalness',
    'liveness',
    'loudness',
    'speechiness',
    'tempo',
    'valence'
]

def plot_frequency_heatmap(filtered_df, era_color_mapping):
    st.header("Frequency of songs played across Eras")
    heatmap_data = filtered_df.groupby(['song_order', 'era_name']).size().reset_index(name='count')
    heatmap_data['color'] = heatmap_data['era_name'].map(era_color_mapping)
    fig_heatmap = px.scatter(heatmap_data, x='song_order', y='count', color='era_name',
                             color_discrete_map=era_color_mapping, size='count',
                             labels={'count': 'Song Play Count'},
                             title='Frequency of songs played across Eras',
                             width=800, height=600)
    st.plotly_chart(fig_heatmap, use_container_width=True)


def plot_live_songs_bar(era_counts, era_color_mapping):
    st.header("Number of Songs performed live by Era")
    fig_bar = px.bar(era_counts, x='era_name', y='count', color='era_name', color_discrete_map=era_color_mapping,
                     labels={'era_name': 'Era', 'count': 'Count'}, title='Number of Songs performed live by Era')
    fig_bar.update_layout(height=500)
    st.plotly_chart(fig_bar, use_container_width=True)

def plot_song_order_swarm(filtered_df, era_color_mapping):
    st.header("Song Order by Era")
    sns.set_theme(style="dark", rc={"grid.color": "#0E1117", 'axes.facecolor': '#0E1117', 'figure.facecolor':'#0E1117',
                                    "axes.edgecolor":'#0E1117', "font.family": "sans-serif", "font.size": 10})
    sns.set_context('talk')
    fig_swarm, ax = plt.subplots(figsize=(10, 5))
    sns.swarmplot(x='song_order', hue='era_name', data=filtered_df, size=3, palette=era_color_mapping.values(),
                  hue_order=era_color_mapping.keys(), ax=ax)
    ax.title.set_position([0.5, 1.05])
    ax.set_title('Song Order by Era', color='white', fontsize=12, fontweight='bold')
    ax.set_xlabel('Song Order', fontsize=12, fontfamily='sans-serif')
    ax.set_ylabel('Era', fontsize=12, fontfamily='sans-serif')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax.set_facecolor('#0E1117')
    ax.tick_params(axis='x', colors='white', labelsize=8)
    ax.tick_params(axis='y', colors='white', labelsize=8)
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    legend = ax.legend(loc='upper left', bbox_to_anchor=(1, 1), facecolor='#0E1117', edgecolor='#0E1117',  fontsize=10)
    for text in legend.get_texts():
        text.set_color('white')
    st.pyplot(fig_swarm)


def plot_musicality_eras_concert(metrics_change_df):

    st.header("Musicality for Eras Concert")
    fig_line = sub_plt.make_subplots(rows=3, cols=3, subplot_titles=metrics)
    for i, column in enumerate(metrics):
        row_position = (i // 3) + 1
        col_position = (i % 3) + 1
        trace = go.Scatter(x=list(range(1, len(metrics_change_df[column])+1)), y=metrics_change_df[column],
                          mode='lines', name=column, line=dict(color='gold'))
        fig_line.add_trace(trace, row=row_position, col=col_position)
    fig_line.update_layout(showlegend=False)
    st.plotly_chart(fig_line, use_container_width=True)


def plot_compare_musicality_cities(filtered_df, selected_city1, selected_city2):
    st.header("Compare Musicality: Cities")
    metrics_change_city_df = filtered_df.groupby(['city', 'song_order']).agg({
        'acousticness': 'mean',
        'danceability': 'mean',
        'energy': 'mean',
        'instrumentalness': 'mean',
        'liveness': 'mean',
        'loudness': 'mean',
        'speechiness': 'mean',
        'tempo': 'mean',
        'valence': 'mean',
        'popularity': 'mean'
    }).reset_index()

    # Check if both cities are selected and have valid data in the DataFrame
    if selected_city1 != 'All' and selected_city2 != 'All' :

        fig_compare_city = sub_plt.make_subplots(rows=3, cols=3, subplot_titles=metrics)

        for i, metric in enumerate(metrics):
            trace_city1 = go.Scatter(x=metrics_change_city_df[(metrics_change_city_df['city'] == selected_city1)]['song_order'],
                                    y=metrics_change_city_df[(metrics_change_city_df['city'] == selected_city1)][metric],
                                    mode='lines', name=f"{selected_city1} - {metric}", line=dict(color='tan'))
            trace_city2 = go.Scatter(x=metrics_change_city_df[(metrics_change_city_df['city'] == selected_city2)]['song_order'],
                                    y=metrics_change_city_df[(metrics_change_city_df['city'] == selected_city2)][metric],
                                    mode='lines', name=f"{selected_city2} - {metric}", line=dict(color='firebrick'))

            fig_compare_city.add_trace(trace_city1, row=(i // 3) + 1, col=(i % 3) + 1)
            fig_compare_city.add_trace(trace_city2, row=(i // 3) + 1, col=(i % 3) + 1)
            fig_compare_city.update_yaxes(zeroline=False, row=(i // 3) + 1, col=(i % 3) + 1)

        fig_compare_city.update_layout(height=600, width=800, showlegend=True, margin=dict(l=10, r=10, b=30, t=100),
                                       title_text=f"Compare Musicality: {selected_city1} vs {selected_city2}")

        st.plotly_chart(fig_compare_city, use_container_width=True)
    else:
        st.warning("Please select two cities with valid data for comparison.")


def plot_popularity_vs_occurrences(song_occurrences, era_color_mapping):

    fig_scatter_popularity = px.scatter(song_occurrences, x='popularity', y='count', color='era_name',
                                        color_discrete_map=era_color_mapping, title='Popularity vs. Song Occurrences',
                                        labels={'popularity': 'Popularity', 'count': 'Song Occurrences'},
                                        hover_data=['era_name'])
    st.plotly_chart(fig_scatter_popularity, use_container_width=True)

def plot_popularity_recorded_songs(recorded_songs_popularity):
    sns.set_theme(style="dark", rc={"grid.color": "#0E1117", 'axes.facecolor': '#0E1117', 'figure.facecolor':'#0E1117',
                                    "axes.edgecolor":'#0E1117', "font.family": "sans-serif", "font.size": 10})
    custom_palette = {True: 'teal', False: 'firebrick'}
    sns.set_context('talk')
    fig_swarm_album, ax = plt.subplots()
    sns.swarmplot(x='album', y='popularity', hue='performed_live', data=recorded_songs_popularity, size=3,
                  palette=custom_palette, ax=ax)
    ax.title.set_position([0.5, 1.05])
    ax.set_facecolor('#0E1117')
    ax.tick_params(axis='x', colors='white', labelsize=8)
    ax.tick_params(axis='y', colors='white', labelsize=8)
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.set_title('Popularity of Recorded Songs by Album', color='white', fontsize=12, fontweight='bold')
    ax.set_xlabel('Album', fontsize=12, fontfamily='sans-serif')
    ax.set_ylabel('Popularity', fontsize=12, fontfamily='sans-serif')
    legend_elements = [Line2D([0], [0], marker='o', color='w', label='Played Live', markerfacecolor='teal', markersize=10),
                       Line2D([0], [0], marker='o', color='w', label='Not Played Live', markerfacecolor='firebrick', markersize=10)]
    legend = ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1), facecolor='#0E1117',
                       edgecolor='#0E1117', fontsize=10)
    for text in legend.get_texts():
        text.set_color('white')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig_swarm_album)


def plot_tickets_sold_across_cities(venue_df):
    st.header("Tickets Sold across cities")
    tickets_sold = venue_df.groupby(['city', 'latitude', 'longitude']).sum()['capacity'].reset_index()
    tickets_sold['capacity_vis'] = tickets_sold['capacity'] // 1000

    st.markdown("<h1 style='text-align: left; color: white; font-size: 20px;'>Tickets Sold across cities</h1>",
                unsafe_allow_html=True)

    scatterplot_layer = pdk.Layer(
        "ScatterplotLayer",
        data=tickets_sold,
        get_position=["longitude", "latitude"],
        get_radius="capacity",
        get_fill_color=[0, 128, 128, 150],
        pickable=True,
        auto_highlight=True,
        hover=True,
        elevation_scale=5,
    )

    deck = pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",
        initial_view_state=pdk.ViewState(
            latitude=venue_df['latitude'].mean(),
            longitude=venue_df['longitude'].mean(),
            zoom=3,
            pitch=0,
        ),
        layers=[scatterplot_layer],
        tooltip={
            "html": "<b>{city}: {capacity_vis}K</b>",
            "style": {
                "backgroundColor": "rgba(255, 255, 255, 0.8)",
                "color": "black",
                "maxWidth": "300px",
                "textAlign": "center",
                "padding": "8px",
                "borderRadius": "4px",
                "boxShadow": "0 0 10px rgba(0, 0, 0, 0.1)",
            }},
    )

    st.pydeck_chart(deck)
