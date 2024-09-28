import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Settings class to load MySQL database configuration from environment variables.
    """

    MYSQL_USER = os.getenv("MYSQL_USER", os.getenv('DB_USER'))
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", os.getenv('DB_PASSWORD'))
    MYSQL_HOST = os.getenv("MYSQL_HOST", os.getenv('DB_HOST'))
    MYSQL_PORT = os.getenv("MYSQL_PORT", os.getenv('DB_PORT'))
    MYSQL_DB = os.getenv("MYSQL_DB", os.getenv('DB_NAME'))

    DATABASE_URL = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@"
        f"{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )

settings = Settings()