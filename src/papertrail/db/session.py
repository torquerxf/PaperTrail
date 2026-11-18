import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Credentials
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:your_actual_password@localhost:5432/papertrail"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)