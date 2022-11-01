from sqlite3 import connect
from sqlmodel import SQLModel, create_engine
from decouple import config

sqlite_file_name = 'hero.db'
sqlite_url = f"sqlite:///{sqlite_file_name}"

postgres_url = config('PG_URL')
connect_args = {
    "check_same_thread": False
}
engine = create_engine(postgres_url, echo=True, )

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)