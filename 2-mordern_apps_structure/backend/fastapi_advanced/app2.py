from fastapi import APIRouter
from typing import Optional

app = APIRouter(prefix="/product", tags=["Product"])

# Dictionary of data
data = {
    1:{
        "name": "product 1",
        "price": "2400XAF",
        "date_posted": "12-6-2025"
    },
    2:{
        "name": "product 2",
        "price": "14000XAF",
        "date_posted": "12-5-2025"
    },
    3:{
        "name": "product 3",
        "price": "13205XAF",
        "date_posted": "12-8-2025"
    }
}
# TOPIC3: QUERY PARAMETER
# WHAT ARE QUERY PARAMETERS? These are parameters
@app.get("/search-product")
def search_product(category: str, page: int, id:Optional[int]=None):
    if id in data:
        fetched = data[id]
    else:
        return {"error": "id doesn't exist"}
    return {
        "data": fetched,
        "category": category,
        "page": page,
        "my_id": id
    }
# def search_product(id: int):
#     if id in data:
#         return{ "data": data[id] }
#     else:
#         return{
#             {"error": "id doesn't exist"}
#         }
