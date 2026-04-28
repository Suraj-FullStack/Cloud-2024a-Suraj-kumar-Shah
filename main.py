
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel, ConfigDict
from typing import List
import os
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://suraj2024a:Kumar3310@surajkumarshah-2024a-db.postgres.database.azure.com:5432/postgres")    
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class QueryModel(Base):
    __tablename__ = "queries"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    query = Column(String, nullable=False)

try:
    
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Error creating tables: {e}")

class Query(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    first_name: str
    last_name: str
    phone_number: str
    query: str

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health check endpoint
@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/queries", response_model=Query)
def create_query(query: Query, db: Session = Depends(get_db)):
    db_query = QueryModel(first_name=query.first_name, last_name=query.last_name, phone_number=query.phone_number, query=query.query)
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query

@app.get("/queries", response_model=List[Query])
def get_queries(db: Session = Depends(get_db)):
    queries = db.query(QueryModel).all()
    if not queries:
        raise HTTPException(status_code=404, detail="No queries found")
    return queries
