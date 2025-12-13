from fastapi import UploadFile, HTTPException
from .exceptions import INVALID_FILE_EXTENTION, INVALID_FILE_SIZE
from time import time_ns

import os


def validate_file(*, file: UploadFile):
  try:
    validate_file_extention(filename=file.filename)
    validate_file_size(size=file.size)
  except HTTPException as e:
    raise e


def validate_file_extention(*, filename: str):
  VALID_EXTENTIONS = ["xlsx", "csv", "json", "parquet", "xls"]

  file_extention = filename.split(".")[-1]

  if file_extention not in VALID_EXTENTIONS:
    raise INVALID_FILE_EXTENTION


def validate_file_size(*, size: int):
  MAX_FILE_SIZE = 104857600  # 100MB - 1024 * 1024 * 100

  if size > MAX_FILE_SIZE:
    raise INVALID_FILE_SIZE


def save_file(*, file: UploadFile) -> str:
  directory = "uploaded_files"
  filename = f"{time_ns()}_{file.filename}"

  full_path = os.path.join(directory, filename)

  if not os.path.exists(directory):
    os.makedirs(directory)

  with open(file=full_path, mode="wb") as f:
    f.write(file.file.read())

  return full_path
