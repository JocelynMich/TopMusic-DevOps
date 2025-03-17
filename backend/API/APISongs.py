from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión a la base de datos
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='K1m_D0kja20KAJ2M',
    database='MUSIC'
)


class Song(BaseModel):
    ranking: int
    song: str
    artist: str
    image_url: str

@app.get("/", response_model=List[Song])
def get_songs():
    cursor = mydb.cursor()
    cursor.execute("SELECT ranking, song, artist, image_url FROM billboard")
    songs = cursor.fetchall()
    cursor.close()
    return [{"ranking": ranking, "song": song, "artist": artist, "image_url": image_url} for ranking, song, artist, image_url in songs]
   