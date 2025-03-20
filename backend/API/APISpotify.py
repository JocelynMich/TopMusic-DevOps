from fastapi import FastAPI
import mysql.connector
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from fastapi.middleware.cors import CORSMiddleware
import os, time


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

SPOTIPY_CLIENT_ID = '6d04e8ce1038469582e5ea5bcb291b4f'
SPOTIPY_CLIENT_SECRET = '3df73498b85141a8ab22e1b325d52af2'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

def connect_to_db():
    retries = 5
    delay = 5  # seconds
    for i in range(retries):
        try:
            mydb = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"), # this matches your service name
                user=os.getenv("DB_USER", "root"),
                port=os.getenv('DB_PORT', '3306'),
                password=os.getenv("DB_PASSWORD", "K1m_D0kja20KAJ2M"),
                database=os.getenv("DB_NAME", "MUSIC")
        )
            return mydb
        except mysql.connector.Error as err:
            print(f"Connection attempt {i + 1} failed: {err}")
            if i < retries - 1:
                time.sleep(delay)
            else:
                raise

mydb = connect_to_db()

@app.get("/")
def create_playlist():

        cursor = mydb.cursor()
        cursor.execute("SELECT song FROM billboard")
        songs = cursor.fetchall()
        cursor.close()
        mydb.close()

            # Initialize Spotipy client
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            scope="playlist-modify-private"
            ))

        user_id = sp.current_user()["id"]

        song_uris = []
        for song in songs:
            result = sp.search(q=f"track:{song[0]}", type="track", limit=1)
            try:
                uri = result["tracks"]["items"][0]["uri"]
                song_uris.append(uri)
            except IndexError:
                print(f"{song[0]} no existe en Spotify. Saltar.")

        playlist = sp.user_playlist_create(user=user_id, name="Top Weekly Songs", public=False)

        sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
        return {"message": "Playlist created successfully", "playlist_url": playlist["external_urls"]["spotify"]}


