import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, app, redirect, request, session, url_for, render_template
import os

app = Flask(__name__)
SCOPE = "playlist-modify-private user-read-private playlist-read-private"
app.secret_key = os.urandom(24)
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
CACHE_HANDLER = spotipy.cache_handler.FlaskSessionCacheHandler(session)



@app.route("/")
def index():
    return render_template("index.html") 

@app.route("/login")
def login():
    auth_manager = SpotifyOAuth(scope=SCOPE, 
                            client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET, 
                            redirect_uri=REDIRECT_URI,
                            cache_handler=CACHE_HANDLER)
    auth_url = auth_manager.get_authorize_url()
    return render_template("login.html", auth_url=auth_url)

@app.route("/callback")
def callback():
    auth_manager = SpotifyOAuth(scope=SCOPE,
                                client_id=CLIENT_ID,
                                client_secret=CLIENT_SECRET,
                                redirect_uri=REDIRECT_URI,
                                cache_handler=CACHE_HANDLER)
    auth_manager.get_access_token(request.args.get("code"))
    return redirect(url_for("profile"))

@app.route("/profile")
def profile():
    auth_manager = SpotifyOAuth(scope=SCOPE,
                                client_id=CLIENT_ID,
                                client_secret=CLIENT_SECRET,
                                redirect_uri=REDIRECT_URI,
                                cache_handler=CACHE_HANDLER)
    if not auth_manager.validate_token(auth_manager.get_cached_token()):
        return redirect(url_for("login"))
    sp = spotipy.Spotify(auth_manager=auth_manager)
    user_profile = sp.current_user()
    return render_template("profile.html", user_profile=user_profile) 

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/playlists")
def playlists():
    auth_manager = SpotifyOAuth(scope=SCOPE,
                                client_id=CLIENT_ID,
                                client_secret=CLIENT_SECRET,
                                redirect_uri=REDIRECT_URI,
                                cache_handler=CACHE_HANDLER)
    if not auth_manager.validate_token(auth_manager.get_cached_token()):
        return redirect(url_for("login"))
    sp = spotipy.Spotify(auth_manager=auth_manager)
    playlists = sp.current_user_playlists()
    return render_template("playlists.html", playlists=playlists)


if __name__ == "__main__":
    app.run(debug=True)