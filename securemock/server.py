# securemock/server.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict
from securemock.mock_store import mock_store

app = FastAPI()

class MockInput(BaseModel):
    path: str
    method: str
    status: int
    response: dict
    expire: Optional[int] = None
    once: Optional[bool] = False
    match_headers: Optional[Dict[str, str]] = None

@app.post("/_register")
def register_mock(mock: MockInput):
    mock_store.add_mock(
        path=mock.path,
        method=mock.method,
        status=mock.status,
        response=mock.response,
        expire=mock.expire,
        once=mock.once,
        match_headers=mock.match_headers
    )
    return {"message": "Mock registered"}

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def mock_handler(request: Request, full_path: str):
    method = request.method
    path = "/" + full_path
    headers = dict(request.headers)

    mock = mock_store.get_mock(path, method, headers)
    if mock:
        return JSONResponse(status_code=mock["status"], content=mock["response"])
    return JSONResponse(status_code=404, content={"error": "Mock not found"})
