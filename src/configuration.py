import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Configuration:
    PERSISTENCE__DATABASE__DATABASE_URL = os.getenv("persistence.database.database_url")
    INITIAL_USER_1__USERNAME = os.getenv("initial_user_1.username")
    INITIAL_USER_1__PASSWORD = os.getenv("initial_user_1.password")
    INITIAL_USER_2__USERNAME = os.getenv("initial_user_2.username")
    INITIAL_USER_2__PASSWORD = os.getenv("initial_user_2.password")
