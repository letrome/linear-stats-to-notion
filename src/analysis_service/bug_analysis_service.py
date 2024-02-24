from datetime import datetime
from typing import Dict, Optional

from src.analysis_service.analysis_service import AnalysisService
from src.notion.last_bug_analysis_page_builder import LastBugAnalysisPageBuilder
from src.properties import Properties


class BugAnalysisService(AnalysisService):
    def __init__(self, properties: Properties):
        super().__init__(
            linear_api_key=properties.linear_api_key,
            notion_api_key=properties.notion_api_key,
            team_key=properties.team_key,
            linear_ticket_request_template=properties.linear_ticket_request_template,
            linear_bug_request_template=properties.linear_bug_request_template,
            linear_cycle_request_template=properties.linear_cycle_request_template
        )

        self._database_id = properties.bug_analysis_db_id
        self._max_nb_tickets = properties.max_nb_tickets_to_analyze

    def run(self) -> None:
        tickets = self._linear_service.get_last_bugs(max_nb_tickets=self._max_nb_tickets)

        nb_tickets = len(tickets)
        tickets_per_status = self._bucket_tickets_per_status(tickets=tickets)
        timedelta = self._compute_timedelta(tickets=tickets)

        notion_payload = LastBugAnalysisPageBuilder(
            database_id=self._database_id,
            team_key=self._team_key,
            inspection_date=self._inspection_date,
            nb_tickets=nb_tickets,
            tickets_per_status=tickets_per_status,
            timedelta=timedelta,
            last_10_tickets=tickets[:10]
        ).build()

        self._notion_service.insert_notion_page(payload=notion_payload)

    @staticmethod
    def _compute_timedelta(tickets: list[Dict]) -> Dict:
        return {
            'delta_created_started': BugAnalysisService._compute_sub_timedelta(
                tickets=tickets, date_keys=['createdAt', 'startedAt']),
            'delta_started_completed': BugAnalysisService._compute_sub_timedelta(
                tickets=tickets, date_keys=['startedAt', 'completedAt']),
            'delta_created_completed': BugAnalysisService._compute_sub_timedelta(
                tickets=tickets, date_keys=['createdAt', 'completedAt'])
        }

    @staticmethod
    def _compute_sub_timedelta(tickets: list[Dict], date_keys: list[str]) -> Optional[Dict]:
        sublist_tickets = BugAnalysisService._sublist_contains_keys(lst=tickets, keys=[date_keys[0], date_keys[1]])
        if len(sublist_tickets) > 0:
            value_hours = 0
            for ticket in sublist_tickets:
                value_hours += (datetime.fromisoformat(ticket[date_keys[1]]) - datetime.fromisoformat(
                    ticket[date_keys[0]])).total_seconds() / 3600.0

            return {
                "value_hours": value_hours / len(sublist_tickets),
                "sample_size": len(sublist_tickets)
            }

    @staticmethod
    def _sublist_contains_keys(lst: list[Dict], keys: list[str]) -> list[Dict]:
        sublist = []
        for item in lst:
            if False not in [key in item.keys() and item[key] is not None for key in keys]:
                sublist.append(item)

        return sublist
