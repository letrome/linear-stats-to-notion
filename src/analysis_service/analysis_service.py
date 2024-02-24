from abc import ABC, abstractmethod
from datetime import datetime, UTC
from typing import Dict, Optional

from src.linear.linear_service import LinearService
from src.notion.notion_service import NotionService


class AnalysisService(ABC):
    def __init__(self, linear_api_key: str, notion_api_key: str, team_key: str,
                 linear_ticket_request_template: Optional[str], linear_bug_request_template: Optional[str],
                 linear_cycle_request_template: Optional[str]):
        self._linear_service = LinearService(api_key=linear_api_key, team_key=team_key,
                                             linear_ticket_request_template=linear_ticket_request_template,
                                             linear_bug_request_template=linear_bug_request_template,
                                             linear_cycle_request_template=linear_cycle_request_template)
        self._notion_service = NotionService(api_key=notion_api_key)
        self._team_key = team_key
        self._inspection_date = datetime.now(tz=UTC)

    @abstractmethod
    def run(self) -> None:
        pass

    @staticmethod
    def _bucket_tickets_per_status(tickets: list[Dict]) -> Dict:
        results = {}
        for ticket in tickets:
            status = ticket['state']['name']
            if status in results:
                results[status].append(ticket)
            else:
                results[status] = [ticket]

        return results
