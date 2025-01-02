# data_processing.py
import pandas as pd

def load_data():
    df = pd.read_csv('ts_data/ts_setlist_spotify_merged_new_eras_renamed.csv')
    venue_df = pd.read_csv('ts_data/venue_coordinates.csv')
    all_songs = pd.read_csv('ts_data/spotify_taylor_swift_full_new.csv')
    return df, venue_df, all_songs

def preprocess_data(df, venue_df):
    df['era_name'] = df.apply(lambda x: 'Intro' if pd.isna(x['era_name']) else x['era_name'], axis=1)
    df['era_name'] = df.apply(lambda x: 'Surprise Songs' if 'surprise' in x['era_name'].lower() else x['era_name'].capitalize(), axis=1)

    merged_df = pd.merge(df, venue_df[['venue_id', 'city']].drop_duplicates(), on='venue_id')
    cleaned_df = merged_df.dropna(subset=['song_name', 'acousticness'])

    metrics_change_df = cleaned_df.groupby(['song_order']).agg({
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

    return cleaned_df, metrics_change_df
