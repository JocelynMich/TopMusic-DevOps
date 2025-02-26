from fastapi import FastAPI
from APIScrape import app as scrape_app
from APISongs import app as songs_app

app = FastAPI()

app.mount("/scrape", scrape_app)
app.mount("/songs", songs_app)