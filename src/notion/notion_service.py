from typing import Dict

from src.http_client import HttpClient


class NotionService:
    def __init__(self, api_key: str):
        headers = {
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28',
            'Authorization': f'Bearer {api_key}'
        }
        self._http_client = HttpClient(headers=headers)

    def insert_notion_page(self, payload: Dict) -> None:
        url = "https://api.notion.com/v1/pages"
        self._http_client.post(url=url, payload=payload)

    def is_cycle_doc_exists(self, database_id, cycle_name) -> bool:
        url = f"https://api.notion.com/v1/databases/{database_id}/query"

        payload = {
            "filter": {
                "property": "Cycle",
                "rich_text": {
                    "equals": cycle_name
                }
            }
        }

        response = self._http_client.post(url=url, payload=payload, response_json_path=['results'])
        return len(response) > 0
