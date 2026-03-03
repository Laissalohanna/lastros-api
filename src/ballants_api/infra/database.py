from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool


class DatabaseSessionManager:
    def __init__(self, database_url: str, echo: bool = False):
        self.engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_pre_ping=True,
            echo=echo,
            future=True,
        )

        self._session_factory = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            future=True,
        )

    def __enter__(self):
        self.session = self._session_factory()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type:
                self.session.rollback()
            else:
                self.session.commit()
        finally:
            self.session.close()
