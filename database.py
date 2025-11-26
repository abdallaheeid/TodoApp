from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# SQL Configs ## 
SQLITE_DATABASE_URL = "sqlite:///./todos.db"

engine = create_engine(
    SQLITE_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)

## Postgres SQL Configs ## 
# Change these if needed
# POSTGRES_USER = "postgres"
# POSTGRES_PASSWORD = "test1234"
# POSTGRES_HOST = "localhost"
# POSTGRES_PORT = "5432"
# POSTGRES_DB = "TodoApplicationDatabase"

# DATABASE_URL = (
#     f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
#     f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
# )

# engine = create_engine(DATABASE_URL, echo=True)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


## MYSQL Configs ## 

# Load environment variables
# load_dotenv()

# MYSQL_USER = os.getenv("MYSQL_USER")
# MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
# MYSQL_HOST = os.getenv("MYSQL_HOST")
# MYSQL_PORT = os.getenv("MYSQL_PORT")
# MYSQL_DB = os.getenv("MYSQL_DB")

# DATABASE_URL = (
#     f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
#     f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
# )

# engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()