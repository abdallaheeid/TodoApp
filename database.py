from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

## SQL Configs ## 
# SQLITE_DATABASE_URL = "sqlite:///./todos.db"

# engine = create_engine(
#     SQLITE_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
# )

## Postgres SQL Configs ## 
# Change these if needed
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "test1234"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_DB = "TodoApplicationDatabase"

DATABASE_URL = (
    f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


## MYSQL Configs ## 
# Change these if needed
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "test1234"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_DB = "TodoApplicationDatabase"

DATABASE_URL = (
    f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()