from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import mysql.connector
import os
import time
from loguru import logger

app = FastAPI()

logger.add("logs/TopMusic.log", rotation="10 MB", retention="30 days", level="INFO")

def create_table_if_not_exists():
    # Metodo para crear una tabla en caso de que no exista en el contenedor
    temp_db = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv('DB_PORT', '3306'),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "K1m_D0kja20KAJ2M"),
        database=os.getenv("DB_NAME", "MUSIC")
    )
    cursor = temp_db.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS billboard (
                ranking INT NOT NULL,
                song VARCHAR(255) NOT NULL,
                artist VARCHAR(255) NOT NULL,
                image_url VARCHAR(255)
            )
        """)
    temp_db.commit()
    cursor.close()
    temp_db.close()
    logger.info("Tabla 'billboard' se ha creado o ya existe en el schema")


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

create_table_if_not_exists()
mydb = connect_to_db()

class Song(BaseModel):
    ranking: int
    song: str
    artist: str
    image_url: str

@app.get("/", response_model=list[Song])
async def scrape_data():
    logger.info("Empezo el proceso de web-scraping")
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
    billboard_url = "https://www.billboard.com/charts/hot-100/"
    response = requests.get(url=billboard_url, headers=header)

    if response.status_code == 200:
        cursor = mydb.cursor()
        logger.info("Limpiando los datos antiguos de la tabla billboard")
        cursor.execute("DELETE FROM billboard")
        mydb.commit()

        soup = BeautifulSoup(response.text, 'html.parser')
        song_name_spans = soup.select("li ul li h3")
        song_names = [song.getText().strip() for song in song_name_spans]
        artist_name_spans = soup.select("ul li.o-chart-results-list__item span.c-label.a-no-trucate")
        artist_names = [artist.getText().strip() for artist in artist_name_spans]
        image_url_spans = soup.select("div ul li div div.lrv-a-crop-1x1 img.c-lazy-image__img")
        image_urls = [image["src"] for image in image_url_spans if image.has_attr("src")]

        song_names = song_names[:15]
        artist_names = artist_names[:15]
        image_urls = image_urls[:15]

        logger.info(f"Scraped {len(song_names)} canciones de la página Billboard")
        for i in range(len(song_names)):
            cursor.execute("""
            INSERT INTO billboard(ranking, song, artist, image_url)
            VALUES (%s, %s, %s, %s)
            """, (i + 1, song_names[i], artist_names[i], image_urls[i]))
        mydb.commit()

        # Prepare the data for the response
        data = []
        for i in range(len(song_names)):
            data.append({
                'ranking': i + 1,
                'song': song_names[i],
                'artist': artist_names[i],
                'image_url': image_urls[i]
            })
        logger.info("El proceso de scraping se completo exitosamente")
        cursor.close()
        return data
    else:
        logger.error(f"Error de recoger datos de la página Billboard: HTTP {response.status_code}")
        return {"error": "Error de recoger datos de la página Billboard"}

