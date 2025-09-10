from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from constants import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


class DBConnectionHandler:
    DB_URL = URL.create(
        drivername="postgresql+psycopg2",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )

    def __init__(self):
        self.engine = create_engine(self.DB_URL, pool_pre_ping=True)
        self.session_maker = sessionmaker(bind=self.engine)
        self.session = None

    def __enter__(self):
        self.session = self.session_maker()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
        finally:
            self.session.close()
            self.session = None

    def execute(self, query: str, params: dict = None, fetch: str = None):
        result = self.session.execute(text(query), params or {})

        if fetch == "all":
            return result.fetchall()
        elif fetch == "one":
            return result.fetchone()
        elif fetch == "val":
            return result.scalar()
        return result
