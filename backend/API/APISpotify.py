from fastapi import FastAPI
import mysql.connector
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def create_playlist():
    
        mydb = mysql.connector.connect(
                host='localhost',
                user='root',
                password='K1m_D0kja20KAJ2M',
                database='MUSIC'
        )

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


