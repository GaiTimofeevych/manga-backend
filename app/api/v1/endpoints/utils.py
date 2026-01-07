from fastapi import APIRouter, UploadFile, File, Depends, status
from app.services import file_service
from app.api.deps import get_current_admin
from app.models.user import User

router = APIRouter()

@router.post("/upload", response_model=dict, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_admin) # Только админ может грузить
):
    """
    Загрузка файла (картинки).
    Возвращает JSON {"url": "/media/..."}
    """
    file_url = await file_service.save_upload_file(file)
    return {"url": file_url}