from fastapi import FastAPI, HTTPException
import utils

app=FastAPI()

print(utils.greet("bhagyashree"))

print(utils.is_even(45))

# items_list=["Book", "Pen", "Notebook", "Laptop"]

# @app.get("/")
# def root():
#     return {"message": "hello"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#     if item_id<0 or item_id>=len(items_list):
#         raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found. Valid IDs are 0 to {len(items_list)-1}")

#     return {"item_id":item_id, "item_name":items_list[item_id]}

# @app.get("/items")
# def read_item(skip:int=1, limit:int=2):
#     return items_list[skip : skip+limit]