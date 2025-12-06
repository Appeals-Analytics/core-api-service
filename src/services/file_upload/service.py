from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

from pydantic import ValidationError
from src.schemas import MessageSchema
import json

import polars as pl


class FileProcessor(ABC):
  def __init__(self, file_path: Path, chunk_size: int = 50000):
    self.file_path = Path(file_path)
    self.chunk_size = chunk_size

    if not self.file_path.exists():
      raise FileNotFoundError(f"Файл не найден: {file_path}")

  @abstractmethod
  def read_data(self) -> pl.DataFrame:
    pass

  def validate_structure(self, df: pl.DataFrame) -> bool:
    required_columns = {"text", "user_id", "external_id", "timestamp"}
    # optional_columns = set()
    all_allowed_columns = required_columns

    df_columns = set(df.columns)

    missing_required = required_columns - df_columns
    if missing_required:
      raise ValueError(
        f"Invalid file structure. Missing required fields: {missing_required}. "
        f"Required fields: {required_columns}. "
        # f"Optional columns: {optional_columns}."
      )

    extra_columns = df_columns - all_allowed_columns
    if extra_columns:
      print(f"Обнаружены дополнительные столбцы (будут проигнорированы): {extra_columns}")
      df = df.select([col for col in df.columns if col in all_allowed_columns])

    return True

  def validate_and_filter_records(self, df: pl.DataFrame) -> List[MessageSchema]:
    valid_records = []

    records = df.to_dicts()

    for idx, record in enumerate(records, start=1):
      try:
        record_data = {
          "text": record.get("text"),
          "user_id": record.get("user_id"),
          "external_id": record.get("external_id"),
          "timestamp": record.get("timestamp"),
        }

        validated = MessageSchema(**record_data)

        if validated.timestamp is None:
          validated.timestamp = datetime.now().isoformat()

        valid_records.append(validated)

      except ValidationError as e:
        for error in e.errors():
          field = ".".join(str(loc) for loc in error["loc"])
          print(f"Ошибка валидации в строке {idx}, поле '{field}': {error['msg']}")
      except Exception as e:
        print(f"Ошибка при обработке строки {idx}: {e}")

    return valid_records

  def process(self) -> Dict[str, Any]:
    print(f"Начало обработки файла: {self.file_path}")

    try:
      df = self.read_data()
      print(f"Прочитано строк: {len(df)}")

      self.validate_structure(df)
      print("Структура файла валидна")

      valid_records = self.validate_and_filter_records(df)

      result = {
        "data": valid_records,
        "metadata": {
          "source_file": str(self.file_path),
          "processed_at": datetime.now().isoformat(),
        },
      }

      print("Обработка завершена успешно")

      return result

    except Exception as e:
      print(f"Ошибка при обработке файла: {e}")
      raise


class CSVProcessor(FileProcessor):
  def read_data(self) -> pl.DataFrame:
    try:
      df = pl.read_csv(
        self.file_path,
        separator=",",
        encoding="utf-8",
        null_values=["", "NULL", "null", "None"],
        truncate_ragged_lines=True,
      )
      return df
    except Exception as e:
      raise ValueError(f"Ошибка чтения CSV файла: {e}")


class ExcelProcessor(FileProcessor):
  def read_data(self) -> pl.DataFrame:
    try:
      df = pl.read_excel(self.file_path, sheet_id=1)
      return df
    except Exception as e:
      raise ValueError(f"Ошибка чтения Excel файла: {e}")


class JSONProcessor(FileProcessor):
  def read_data(self) -> pl.DataFrame:
    try:
      with open(self.file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

      if not isinstance(data, list):
        df = pl.read_ndjson(self.file_path)
      else:
        df = pl.DataFrame(data)

      return df
    except json.JSONDecodeError:
      try:
        df = pl.read_ndjson(self.file_path)
        return df
      except Exception as e:
        raise ValueError(f"Ошибка чтения JSON файла: {e}")
    except Exception as e:
      raise ValueError(f"Ошибка чтения JSON файла: {e}")


class ParquetProcessor(FileProcessor):
  def read_data(self) -> pl.DataFrame:
    try:
      df = pl.read_parquet(self.file_path)
      return df
    except Exception as e:
      raise ValueError(f"Ошибка чтения Parquet файла: {e}")


class FileProcessorFactory:
  _processors = {
    ".csv": CSVProcessor,
    ".xlsx": ExcelProcessor,
    ".xls": ExcelProcessor,
    ".json": JSONProcessor,
    ".jsonl": JSONProcessor,
    ".parquet": ParquetProcessor,
  }

  @classmethod
  def create_processor(cls, file_path: Path, chunk_size: int = 50000) -> FileProcessor:
    file_path = Path(file_path)
    extension = file_path.suffix.lower()

    processor_class = cls._processors.get(extension)
    if processor_class is None:
      raise ValueError(
        f"Неподдерживаемый формат файла: {extension}. Поддерживаются: {list(cls._processors.keys())}"
      )

    return processor_class(file_path, chunk_size)


def process_file(file_path: str) -> Dict[str, Any]:
  processor = FileProcessorFactory.create_processor(Path(file_path))
  return processor.process()


def validate_file_structure(file_path: str) -> None:
  processor = FileProcessorFactory.create_processor(Path(file_path))
  df = processor.read_data()
  processor.validate_structure(df)
