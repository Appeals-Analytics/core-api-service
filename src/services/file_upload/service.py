from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

from pydantic import ValidationError
from src.schemas import MessageSchema
import polars as pl


class FileProcessor(ABC):
    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    @abstractmethod
    def read_data(self) -> pl.DataFrame:
        pass

    def validate_structure(self, df: pl.DataFrame) -> None:
        required_columns = {"text", "user_id", "external_id", "timestamp"}
        missing = required_columns - set(df.columns)
        if missing:
            raise ValueError(f"Отсутствуют обязательные колонки: {', '.join(missing)}. Пожалуйста, проверьте структуру файла.")

    def _handle_validation_error(self, row_num: int, error: ValidationError) -> None:
        messages = []
        for err in error.errors():
            loc = err["loc"]
            field = str(loc[0]) if loc else "unknown"
            err_type = err["type"]
            
            msg = f"Поле '{field}' содержит ошибку"
            solution = "Проверьте корректность данных"

            if field == "text":
                if err_type in ("string_type", "missing"):
                    msg = "Поле 'text' (текст обращения) не заполнено"
                    solution = "Убедитесь, что в столбце 'text' есть текст обращения"
                elif "min_length" in err_type or "value_error" in err_type:
                    msg = "Поле 'text' пустое"
                    solution = "Текст обращения не может быть пустым"
            
            elif field == "timestamp":
                msg = "Неверный формат даты/времени"
                solution = "Используйте формат ISO 8601 (например, 2023-12-31T23:59:59)"
            
            messages.append(f"{msg}. Решение: {solution}")

        final_msg = f"Ошибка валидации в строке {row_num}: {'; '.join(messages)}"
        raise ValueError(final_msg)

    def validate_content(self, df: pl.DataFrame) -> None:
        try:
            records = df.to_dicts()
            for i, record in enumerate(records):
                clean_record = {k: (v if v is not None else None) for k, v in record.items()}
                
                if isinstance(clean_record.get("timestamp"), datetime):
                    clean_record["timestamp"] = clean_record["timestamp"].isoformat()
                
                MessageSchema(**clean_record)
        except ValidationError as e:
            self._handle_validation_error(i + 1, e)
        except Exception as e:
            raise ValueError(f"Ошибка обработки строки {i+1}: {e}")

    def process(self) -> Dict[str, Any]:
        df = self.read_data()
        self.validate_structure(df)
        self.validate_content(df)

        records = df.to_dicts()
        valid_records = []
        
        for record in records:
            clean_record = {k: (v if v is not None else None) for k, v in record.items()}
            
            if isinstance(clean_record.get("timestamp"), datetime):
                clean_record["timestamp"] = clean_record["timestamp"].isoformat()
            
            if not clean_record.get("timestamp"):
                clean_record["timestamp"] = datetime.now().isoformat()
                
            valid_records.append(MessageSchema(**clean_record))

        return {
            "data": valid_records,
            "metadata": {
                "source_file": str(self.file_path),
                "processed_at": datetime.now().isoformat(),
            },
        }


class CSVProcessor(FileProcessor):
    def read_data(self) -> pl.DataFrame:
        try:
            return pl.read_csv(self.file_path, separator=",", ignore_errors=False)
        except Exception as e:
            raise ValueError(f"Ошибка чтения CSV файла: {e}. Убедитесь, что файл имеет корректный формат CSV.")


class ExcelProcessor(FileProcessor):
    def read_data(self) -> pl.DataFrame:
        try:
            return pl.read_excel(self.file_path)
        except Exception as e:
            raise ValueError(f"Ошибка чтения Excel файла: {e}. Убедитесь, что файл не поврежден.")


class JSONProcessor(FileProcessor):
    def read_data(self) -> pl.DataFrame:
        try:
            return pl.read_json(self.file_path)
        except Exception:
            try:
                return pl.read_ndjson(self.file_path)
            except Exception as e:
                raise ValueError(f"Ошибка чтения JSON файла: {e}. Проверьте синтаксис JSON.")


class ParquetProcessor(FileProcessor):
    def read_data(self) -> pl.DataFrame:
        try:
            return pl.read_parquet(self.file_path)
        except Exception as e:
            raise ValueError(f"Ошибка чтения Parquet файла: {e}. Убедитесь, что файл не поврежден.")


class FileProcessorFactory:
    _processors = {
        ".csv": CSVProcessor,
        ".xlsx": ExcelProcessor,
        ".xls": ExcelProcessor,
        ".json": JSONProcessor,
        ".parquet": ParquetProcessor,
    }

    @classmethod
    def create(cls, file_path: Path) -> FileProcessor:
        ext = file_path.suffix.lower()
        processor = cls._processors.get(ext)
        if not processor:
            raise ValueError(f"Неподдерживаемый формат файла: {ext}. Поддерживаемые форматы: {', '.join(cls._processors.keys())}")
        return processor(file_path)


def process_file(file_path: str) -> Dict[str, Any]:
    return FileProcessorFactory.create(Path(file_path)).process()


def validate_file_structure(file_path: str) -> None:
    processor = FileProcessorFactory.create(Path(file_path))
    df = processor.read_data()
    processor.validate_structure(df)
    processor.validate_content(df)

