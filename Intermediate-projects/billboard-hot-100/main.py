import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
load_dotenv()

SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
OAUTH_AUTHORIZE_URL= 'https://accounts.spotify.com/authorize'
OAUTH_TOKEN_URL= 'https://accounts.spotify.com/api/token'
SPOTIFY_REDIRECT_URI = 'http://127.0.0.1:9090'


auth_manager = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET, 
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="playlist-modify-private playlist-modify-public"
)

#playlist_add_items(playlist_id, items, position=None)

sp = spotipy.Spotify(auth_manager=auth_manager)

current_user = sp.current_user()['id']

playlist = sp.user_playlist_create(current_user, '2025-playlist', public=False, description="python-project-paylist" )
playlist_id = playlist['id']


header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"}

data = requests.get(headers=header, url = f"https://www.billboard.com/charts/year-end/2025/billboard-global-200/").text

soup = BeautifulSoup(data, "html.parser")

raw_song_titles = soup.find_all(name="h3", id="title-of-a-story")

song_titles = [song.getText().strip() for song in raw_song_titles]

print(len(song_titles))

for song in song_titles:
    search = sp.search(q=f"{song}", type="track", limit=1)
    if search['tracks']['items']:
        track_uri = search['tracks']['items'][0]['uri']
        result = sp.playlist_add_items(playlist_id, [track_uri])
    else:
        print("no track found")
