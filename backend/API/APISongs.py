from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import os, time
from loguru import logger
from pathlib import Path


app = FastAPI()

LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

log_file = LOGS_DIR / f"{Path(__file__).stem}.log"
logger.add(log_file, rotation="10 MB", retention="30 days", level="INFO", enqueue=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def connect_to_db():
    retries = 5
    delay = 10  # seconds
    for i in range(retries):
        try:
            mydb = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"), # this matches your service name
                user=os.getenv("DB_USER", "root"),
                port=os.getenv('DB_PORT', '3306'),
                password=os.getenv("DB_PASSWORD", "K1m_D0kja20KAJ2M"),
                database=os.getenv("DB_NAME", "MUSIC")
        )
            logger.info("Connectado a la base de datos exitosamente")
            return mydb
        except mysql.connector.Error as err:
            logger.error(f"Intento de conexión {i + 1} fallido: {err}")
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
    try:
        cursor = mydb.cursor()
        logger.info("Recogiendo datos de la base de datos")
        cursor.execute("SELECT ranking, song, artist, image_url FROM billboard")
        songs = cursor.fetchall()
        cursor.close()

        # Agrega logs para depuración
        logger.info(f"Datos obtenidos {len(songs)} de canciones de la base de datos")
        return [{"ranking": ranking, "song": song, "artist": artist, "image_url": image_url} for ranking, song, artist, image_url in songs]
    except Exception as e:
        print(f"Error fetching songs: {e}")
        return {"error": "An error occurred while fetching songs"}