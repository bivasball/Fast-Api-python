import os
from dotenv import load_dotenv
from pathlib import Path

# Determine which environment to load
env_name = os.getenv("ENV", "dev")  # Default to 'dev' if ENV is not set
dotenv_path = Path(f".env.{env_name}")

# Check if the file exists
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
else:
    print(f"⚠️ Warning: {dotenv_path} file not found!")

# Retrieve environment variables
DATABASE_HOSTNAME = os.getenv("DATABASE_HOSTNAME")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", 5432))  # Default to 5432 if not set
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Debugging output (optional)
print(f"Loaded config from: {dotenv_path}")
print(f"Database: {DATABASE_HOSTNAME}:{DATABASE_PORT}, User: {DATABASE_USERNAME}")


"""
import os

# print(os.path.exists("app/.env"))
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
"""
