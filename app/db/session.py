from sqlmodel import create_engine, Session
from app.core.config import config

engine = create_engine(config.database_url, echo=config.debug)

def get_session():
    with Session(engine) as session:
        yield session
