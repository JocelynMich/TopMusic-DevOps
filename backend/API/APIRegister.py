from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
import mysql.connector
import os,time
from loguru import logger
from pathlib import Path

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

class UserRegister(BaseModel):
    username: str
    password: str
    role: str 

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


@app.post("/")
def register_user(user: UserRegister):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        # Verifica si el usuario ya existe
        cursor.execute("SELECT * FROM users WHERE username = %s", (user.username,))
        if cursor.fetchone():
            logger.info("El usuario existe en la tabla")

        # Hashea la contraseña
        logger.info("Hashear la contraseña")
        hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

        # Inserta el usuario
        logger.info("Insertar el usuario a la tabla de usuarios")

        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                       (user.username, hashed_pw.decode('utf-8'), user.role))
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Usuario '{user.username}' registrado correctamente con rol '{user.role}'")
        return {"message": "Usuario registrado correctamente"}
    except Exception as e:
        logger.error(f"Error al registrar usuario '{user.username}': {e}")

