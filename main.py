from fastapi import FastAPI
from api import users, products, categories, stocks 
from database import engine
from models import Base  
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(stocks.router, prefix="/stocks", tags=["stocks"])

@app.get("/")
def read_root():
    return {"Hello": "World"}
