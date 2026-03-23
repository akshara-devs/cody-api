import os

from dotenv import load_dotenv


# Load local environment variables before reading settings.
load_dotenv()


class Settings:
    def __init__(self) -> None:
        self.database_url = self._normalize_database_url(
            os.getenv("DATABASE_URL", "")
        )

    @staticmethod
    def _normalize_database_url(database_url: str) -> str:
        # Use the installed psycopg v3 driver when the URL omits a driver name.
        if database_url.startswith("postgresql://"):
            return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
        return database_url


settings = Settings()
