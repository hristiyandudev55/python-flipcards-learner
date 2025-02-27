import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")
DB_TEST_URL = os.getenv("TEST_DB_URL")

AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")
