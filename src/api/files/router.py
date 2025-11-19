from fastapi import APIRouter, UploadFile

from api.files.utils import validate_file, save_file

files_router = APIRouter(prefix="/files", tags=["File"])

@files_router.post("/upload")
async def upload_file(file: UploadFile):
  
  validate_file(file=file)
  
  save_file(file=file)
  
  
@files_router.post("/multiple-upload")
async def upload_files(files: list[UploadFile]):
  
  for file in files:
    await upload_file(file=file)