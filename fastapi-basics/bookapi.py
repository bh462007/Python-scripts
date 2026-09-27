from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

class Book(BaseModel):
    title:str
    author:str
    price:int

@app.post("/book")
def create_book(book: Book):
    return book