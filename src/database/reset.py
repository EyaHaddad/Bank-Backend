from src.database.core import engine
from src.database.models import Base

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("Database reset done.")
