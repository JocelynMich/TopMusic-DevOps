from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
import mysql.connector
import os,time
from loguru import logger
from pathlib import Path
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, Header

app = FastAPI()

LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

log_file = LOGS_DIR / f"{Path(__file__).stem}.log"
logger.add(log_file, rotation="10 MB", retention="30 days", level="INFO", enqueue=True)

logger.info("Probando escritura en archivo de log")

def connect_to_db():
    retries = 5
    delay = 10  # seconds
    for i in range(retries):
        try:
            mydb = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"), 
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

class UserLogin(BaseModel):
    username: str
    password: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#ENCRIPTAR LOS DATOS
SECRET_KEY = "2530"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str = Header(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

@app.post("/")
def login_user(user: UserLogin):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        logger.info("Recolectando datos de los usuarios")
        cursor.execute("SELECT password, role FROM users WHERE username = %s", (user.username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if not result:
            logger.warning(f"Intento de login fallido: usuario '{user.username}' no encontrado")
            raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

        hashed_password, role = result
        if bcrypt.checkpw(user.password.encode('utf-8'), hashed_password.encode('utf-8')):
            token_data = {"sub": user.username, "role": role}
            token = create_access_token(token_data)
            logger.info(f"Usuario '{user.username}' inició sesión correctamente con rol '{role}'")
            return {"access_token": token, "token_type": "bearer", "role": role}
        else:
            logger.warning(f"Intento de login fallido: contraseña incorrecta para usuario '{user.username}'")
            raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    except Exception as e:
        logger.error(f"Error durante el login de usuario '{user.username}': {e}")
        raise HTTPException(status_code=500, detail=str(e))