from sqlmodel import Session, create_engine

from app.core.config import settings

engine = create_engine(settings.database_url, echo=True)

engine = create_engine(config.database_url, echo=config.debug)

def get_session():
    with Session(engine) as session:
        yield session