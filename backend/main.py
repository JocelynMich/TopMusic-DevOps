from fastapi import FastAPI
from API.APIScrape import app as scrape_app
from API.APISongs import app as songs_app
from API.APISpotify import app as spotify_app
from API.APIRegister import app as register_app
from API.APILogin import app as login_app
from prometheus_client import make_asgi_app, Counter, Histogram
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, Header

app = FastAPI()

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

REQUEST_COUNTER = Counter(
    "http_requests_total",
    "Total de solicitudes HTTP",
    ["method", "endpoint", "status_code"]
)

REQUEST_LATENCY  = Histogram(
    "http_request_duration_seconds",
    "Latencia de las solicitudes HTTP",
    ["method", "endpoint"]
)
@app.middleware("http")
async def monitor_requests(request, call_next):
    method = request.method
    endpoint = request.url.path
    
    # Mide tiempo de ejecución
    with REQUEST_LATENCY .labels(method, endpoint).time():
        response = await call_next(request)
    
    # Registra la solicitud
    REQUEST_COUNTER.labels(method, endpoint, response.status_code).inc()
    return response


app.mount("/scrape", scrape_app)
app.mount("/songs", songs_app)
app.mount("/create_playlist", spotify_app)
app.mount("/register", register_app)
app.mount("/login", login_app)