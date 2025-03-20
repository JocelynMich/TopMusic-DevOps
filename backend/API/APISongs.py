from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from typing import List
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

def connect_to_db():
    retries = 5
    delay = 5  # seconds
    for i in range(retries):
        try:
            mydb = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"), # this matches your service name
                user=os.getenv("DB_USER", "root"),
                port=os.getenv('DB_PORT', '3307'),
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
   