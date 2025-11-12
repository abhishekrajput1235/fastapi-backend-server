from fastapi import FastAPI
from sqlalchemy import text
from app.core.database import engine
from app.routes import auth_routes, user_routes,server_routes


app = FastAPI()

# Startup event to test DB connection
@app.on_event("startup")
def startup_event():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("✅ Database connected successfully!")
    except Exception as e:
        print("❌ Database connection failed!")
        print("Error:", e)



app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(server_routes.router)



@app.get("/")
def root():
    return {"message": "FastAPI running with PostgreSQL"}
