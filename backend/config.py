import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Variável de ambiente SECRET_KEY não definida")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("Variável de ambiente DATABASE_URL não definida")

ALGORITHM = os.getenv("ALGORITHM", "HS256")
