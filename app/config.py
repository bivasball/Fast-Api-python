import os
print(os.path.exists(".env"))
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path("app/.env") 
load_dotenv(dotenv_path=dotenv_path)
if not load_dotenv(dotenv_path=dotenv_path):
    print("Failed to load .env file.")


DATABASE_HOSTNAME = os.getenv("DATABASE_HOSTNAME")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", 5432))  # Default to 5432 if not set
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


