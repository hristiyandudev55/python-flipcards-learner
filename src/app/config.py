import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")
DB_TEST_URL = os.getenv("TEST_DB_URL")
