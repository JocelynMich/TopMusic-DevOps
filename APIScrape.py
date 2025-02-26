from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime

app = FastAPI()


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

@app.get("/", response_model=list[Song])
async def scrape_data():
    # Simular un navegador para evitar bloqueos
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
    billboard_url = "https://www.billboard.com/charts/hot-100/"
    response = requests.get(url=billboard_url, headers=header)

    if response.status_code == 200:
        cursor = mydb.cursor()
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

        extraction_date = datetime.now().strftime('%Y-%m-%d')

        # Insertar los datos en la base de datos
        for i in range(len(song_names)):
            cursor.execute("""
            INSERT INTO billboard(ranking, song, artist, image_url, extraction_date)
            VALUES (%s, %s, %s, %s, %s)
            """, (i + 1, song_names[i], artist_names[i], image_urls[i], extraction_date))
        mydb.commit()

        # Preparar los datos para la respuesta
        data = []
        for i in range(len(song_names)):
            data.append({
                'ranking': i + 1,
                'song': song_names[i],
                'artist': artist_names[i],
                'image_url': image_urls[i]
                
            })
            cursor.close()
        return data
    

    

