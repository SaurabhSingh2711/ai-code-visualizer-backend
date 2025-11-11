from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/")
async def analyze_code(file: UploadFile = File(...)):
    return {"message": f"Received file: {file.filename}"}
