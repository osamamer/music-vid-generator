# lyrics_fetcher.py - Module to fetch lyrics from Spotify API and PHP-based Lyrics API

import os
import requests
import base64

# Get Spotify API credentials from environment variables
CLIENT_ID = "013bc4ef9aaf4b4489799478a07c32b1"
CLIENT_SECRET = "5fb33bf6228a47059d8a488bb201bea5"

def get_spotify_access_token():
    """Authenticate and get an access token from Spotify API."""
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: Missing Spotify API credentials.")
        return None

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    }
    data = {"grant_type": "client_credentials"}

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.RequestException as e:
        print(f"Error fetching Spotify access token: {e}")
        return None

def get_track_id(song_title, artist_name):
    """Fetch Spotify track ID using song title and artist name."""
    access_token = get_spotify_access_token()
    if not access_token:
        return None

    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": f"track:{song_title} artist:{artist_name}", "type": "track", "limit": 1}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        tracks = response.json().get("tracks", {}).get("items", [])
        if not tracks:
            return None  # No matching track found
        return tracks[0]["id"]  # Return first matching track ID
    except requests.RequestException as e:
        print(f"Error fetching track ID: {e}")
        return None

def fetch_lyrics_from_php_api(song_title, artist_name):
    """Fetch lyrics using track ID from Spotify and the PHP-based Lyrics API."""
    track_id = get_track_id(song_title, artist_name)
    if not track_id:
        print("Could not find track ID on Spotify.")
        return None

    base_url = "http://localhost:8000/"  # Change if hosted remotely
    params = {"trackid": track_id}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("lyrics", "Lyrics not found.")
    except requests.RequestException as e:
        print(f"Error fetching lyrics: {e}")
        return None
