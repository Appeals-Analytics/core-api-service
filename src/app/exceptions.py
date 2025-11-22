from fastapi import HTTPException, status

def BAD_REQUEST_EXCEPTION(detail: str) -> HTTPException:
  return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

def INTERNAL_SERVER_ERROR_EXCEPTION(detail: str) -> HTTPException:
  return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

def FORRBIDEN_ERROR_EXCEPTION(detail: str) -> HTTPException:
  return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

def UNAUTHORIZED_EXCEPTION(detail: str) -> HTTPException:
  return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

def CONTENT_TOO_LARGE_EXCEPTION(detail: str) -> HTTPException:
  return HTTPException(status_code=status.HTTP_413_CONTENT_TOO_LARGE, detail=detail)

def RAISE_ERROR_EXCEPTION(detail: str) -> RuntimeError:
  return RuntimeError(detail)