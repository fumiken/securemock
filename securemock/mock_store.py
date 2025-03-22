import time
import json
import os
from typing import Dict, Any, Optional
from threading import Lock


class MockStore:
    def __init__(self, storage_path="mock_data.json"):
        self._store: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
        self._storage_path = storage_path
        self.load_from_file()

    def _generate_key(self, path: str, method: str) -> str:
        return f"{method.upper()}::{path}"

    def add_mock(
        self,
        path: str,
        method: str,
        response: dict,
        status: int = 200,
        expire: Optional[int] = None,
        once: bool = False,
        match_headers: Optional[Dict[str, str]] = None
    ):
        key = self._generate_key(path, method)
        expire_at = time.time() + expire if expire else None

        with self._lock:
            self._store[key] = {
                "status": status,
                "response": response,
                "expire_at": expire_at,
                "once": once,
                "match_headers": match_headers or {}
            }
            self.save_to_file()

    def get_mock(self, path: str, method: str, request_headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
        key = self._generate_key(path, method)
        mock = self._store.get(key)

        if not mock:
            return None

        # Expired mock
        if mock.get("expire_at") and time.time() > mock["expire_at"]:
            self.delete_mock(path, method)
            return None

        # Normalize headers to lowercase
        lowercase_headers = {k.lower(): v for k, v in request_headers.items()}
        match_headers = mock.get("match_headers", {})

        for k, v in match_headers.items():
            if lowercase_headers.get(k.lower()) != v:
                return None

        # If once is set, delete after first match
        if mock.get("once"):
            self.delete_mock(path, method)

        return mock

    def delete_mock(self, path: str, method: str):
        key = self._generate_key(path, method)
        with self._lock:
            if key in self._store:
                del self._store[key]
                self.save_to_file()

    def save_to_file(self):
        with open(self._storage_path, "w") as f:
            json.dump(self._store, f, indent=2)

    def load_from_file(self):
        if os.path.exists(self._storage_path):
            with open(self._storage_path, "r") as f:
                self._store = json.load(f)

mock_store = MockStore()
