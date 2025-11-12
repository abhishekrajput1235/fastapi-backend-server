from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os


load_dotenv()
# Your PostgreSQL URL
DATABASE_URL: str = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine
try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("✅ Database connected successfully!")
    connection.close()
except Exception as e:
    print("❌ Database connection failed!")
    print("Error:", e)

# Session & Base setup
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency for routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
