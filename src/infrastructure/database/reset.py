"""Database reset utility."""

from src.infrastructure.database import Base, get_engine

engine = get_engine()

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

#print("Database removed successfully.")
print("Database reset done.")
#print(engine.url)
