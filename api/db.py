import os
import time

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def wait_for_db(retries, delay):
    for attempt in range(1, retries + 1):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                print("Database is ready!")
                return
        except OperationalError as e:
            print(f"Database is not ready yet (attempt {attempt}/{retries}): {e}")
            if attempt == retries:
                print("Max retries reached. Exiting.")
                raise
            time.sleep(delay)
