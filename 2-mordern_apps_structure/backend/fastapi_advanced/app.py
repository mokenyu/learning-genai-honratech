from fastapi import UploadFile, Form, File, APIRouter

app = APIRouter(prefix="/profile", tags=["Profile"])

@app.post("/test")
def test_point(file: UploadFile = File(...), status: bool = Form(default=True)):
    return {"file": file, "status": status}