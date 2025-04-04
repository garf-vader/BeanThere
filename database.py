from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env file into environment variables

# Database connection details
dialect = "mysql"
driver = "pymysql"
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
hostname = os.getenv("DB_HOST")  # fallback to localhost
port = os.getenv("DB_PORT")           # default MySQL port
database = os.getenv("DB_NAME")

# Construct the full database URL
DATABASE_URL = f"{dialect}+{driver}://{username}:{password}@{hostname}:{port}/{database}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()