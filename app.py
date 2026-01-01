import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, redirect, request, session, url_for
import os
from dotenv import load_dotenv

scope = "user-library-read"

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=os.getenv("SPOTIPY_CLIENT_ID"), client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"), redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI")))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(f"{idx + 1}. {track['artists'][0]['name']} – {track['name']}")