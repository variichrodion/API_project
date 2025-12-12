from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/restaurant_db"
engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session