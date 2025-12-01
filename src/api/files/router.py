from fastapi import APIRouter, UploadFile, BackgroundTasks, status

from src.api.files.utils import validate_file, save_file
from src.api.files.service import FilesService

files_router = APIRouter(prefix="/files", tags=["File"])


@files_router.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_file(file: UploadFile, background_tasks: BackgroundTasks):
    validate_file(file=file)

    saved_path = save_file(file=file)

    background_tasks.add_task(FilesService.process_and_send_to_kafka, saved_path)

    return {"status": "processing"}


@files_router.post("/multiple-upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_files(files: list[UploadFile], background_tasks: BackgroundTasks):
    for file in files:
        validate_file(file=file)
        saved_path = save_file(file=file)
        background_tasks.add_task(FilesService.process_and_send_to_kafka, saved_path)
    return {"status": "processing"}
