from databases import Database
from src.config import settings

database = Database(url=settings.DATABASE_URL, min_size=5, max_size=20)