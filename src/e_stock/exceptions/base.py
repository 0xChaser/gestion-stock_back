from fastapi import Request
from fastapi.responses import JSONResponse

class Error(Exception):
    message: str

class NotFound(Error):
    def __init__(self, message: str):
        super().__init__(message)

async def not_found_exception_handler(request: Request, exc: NotFound):
    return JSONResponse(status_code=404, content={"error": exc.message})

def register_handlers(app):
    @app.exception_handler(NotFound)
    async def not_found_exception_handler(request: Request, exc: NotFound):
        return JSONResponse(status_code=404, content={"error": exc.message})