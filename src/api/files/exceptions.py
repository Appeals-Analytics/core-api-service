from src.exceptions import BAD_REQUEST_EXCEPTION, CONTENT_TOO_LARGE_EXCEPTION

INVALID_FILE_EXTENTION = BAD_REQUEST_EXCEPTION("Invalid file extention was provided")
INVALID_FILE_SIZE = CONTENT_TOO_LARGE_EXCEPTION("Invalid file size was provided")