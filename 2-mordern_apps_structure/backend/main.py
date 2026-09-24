from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_advanced.app import app as profile_router
from fastapi_advanced.app2 import app as product_router
from first_app import app as multi_router

app = FastAPI(title="Route Database")

cors_origins = [
    "http://localhost:3000",
    "http://localhost:5123",
    "http://localhost:8501",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5123",
    "http://127.0.0.1:8501",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile_router)
app.include_router(product_router)
app.include_router(multi_router)

@app.get("/") # Decorator - @ # HTTP method: GET, POST
def home(action: str):
    """ This endpoint is used to expose the root. It needs an action parameter. """ # Docstring
    return {"status": "online", "system": "Hello World", "action": action}