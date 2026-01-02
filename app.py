import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, app, redirect, request, session, url_for, render_template
import os

app = Flask(__name__)
SCOPE = "user-library-read"
app.secret_key = os.urandom(24)



# load_dotenv()

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, 
#                                                client_id=os.getenv("SPOTIPY_CLIENT_ID"),
#                                                client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"), 
#                                                redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI")))

# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(f"{idx + 1}. {track['artists'][0]['name']} – {track['name']}")
@app.route("/")
def index():
    return render_template("index.html") 

@app.route("/login")
def login():
    auth_manager = SpotifyOAuth(scope=SCOPE, 
                            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"), 
                            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
                            cache_handler=spotipy.cache_handler.FlaskSessionCacheHandler(session))
    auth_url = auth_manager.get_authorize_url()
    return render_template("login.html", auth_url=auth_url)

@app.route("/callback")
def callback():
    auth_manager = SpotifyOAuth(scope=SCOPE,
                                client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                                client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                                redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
                                cache_handler=spotipy.cache_handler.FlaskSessionCacheHandler(session))
    auth_manager.get_access_token(request.args.get("code"))
    return redirect(url_for("profile"))

@app.route("/profile")
def profile():
    auth_manager = SpotifyOAuth(scope=SCOPE,
                                client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                                client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                                redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
                                cache_handler=spotipy.cache_handler.FlaskSessionCacheHandler(session))
    if not auth_manager.validate_token(auth_manager.get_cached_token()):
        return redirect(url_for("login"))
    sp = spotipy.Spotify(auth_manager=auth_manager)
    user_profile = sp.current_user()
    return f"Logged in as: {user_profile['display_name']}"


if __name__ == "__main__":
    app.run(debug=True)