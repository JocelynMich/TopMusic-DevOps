from fastapi import FastAPI
from API.APIScrape import app as scrape_app
from API.APISongs import app as songs_app
from API.APISpotify import app as spotify_app

app = FastAPI()

app.mount("/scrape", scrape_app)
app.mount("/songs", songs_app)
app.mount("/create_playlist", spotify_app)