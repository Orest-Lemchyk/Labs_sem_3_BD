import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '12345678')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'spotify')

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

ECHO_SQL = os.getenv('SQLALCHEMY_ECHO', 'false').lower() == 'true'
engine = create_engine(DATABASE_URL, echo=ECHO_SQL)

Base = declarative_base()

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
