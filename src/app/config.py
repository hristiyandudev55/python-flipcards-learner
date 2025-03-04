import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()


DB_TEST_URL = os.getenv("TEST_DB_URL")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD", ""))
DB_URL = os.getenv("DATABASE_URL")

if not DB_URL:
    DB_URL = f"postgresql://{os.getenv('DB_USER')}:{DB_PASSWORD}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?sslmode=require"

AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")

