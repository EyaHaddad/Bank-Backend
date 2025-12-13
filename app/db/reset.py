from app.db.session import engine
from app.db.models import Base

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("Database reset done.")
