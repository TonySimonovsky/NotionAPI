import requests
from typing import Dict, Any, Optional
from .data import *

class NotionAPI:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.notion.com/v1"
        self.database = Database(self)

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

class Database:
    def __init__(self, api: NotionAPI):
        self.api = api

    def query(self, database_id: str, query: Optional[Dict[str, Any]] = None) -> DatabaseQuery:
        url = f"{self.api.base_url}/databases/{database_id}/query"
        headers = self.api._get_headers()
        response = requests.post(url, headers=headers, json=query or {})
        response.raise_for_status()
        return DatabaseQuery(**response.json())

