from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.upload_service import UploadService

upload_router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

upload_service = UploadService()

@upload_router.post("/file")
async def upload_file(file: UploadFile = File(...)):
    try:
        saved_path = await upload_service.save_file(file)
        return {"status": "success", "path": saved_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@upload_router.post("/zip")
async def upload_zip(file: UploadFile = File(...)):
    try:
        extract_path = await upload_service.extract_zip(file)
        return {"status": "success", "path": extract_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
