from typing import Dict

from src.analysis_service.analysis_service import AnalysisService
from src.notion.last_ticket_analysis_page_builder import LastTicketAnalysisPageBuilder
from src.properties import Properties


class TicketAnalysisService(AnalysisService):
    def __init__(self, properties: Properties):
        super().__init__(
            linear_api_key=properties.linear_api_key,
            notion_api_key=properties.notion_api_key,
            team_key=properties.team_key,
            linear_ticket_request_template=properties.linear_ticket_request_template,
            linear_bug_request_template=properties.linear_bug_request_template,
            linear_cycle_request_template=properties.linear_cycle_request_template
        )

        self._database_id = properties.ticket_analysis_db_id
        self._max_nb_tickets = properties.max_nb_tickets_to_analyze

    def run(self) -> None:
        tickets = self._linear_service.get_last_tickets(max_nb_tickets=self._max_nb_tickets)

        nb_tickets = len(tickets)
        tickets_per_status = self._bucket_tickets_per_status(tickets=tickets)
        tickets_per_description_status = self._bucket_tickets_per_description_status(tickets=tickets)
        tickets_per_type = self._bucket_tickets_per_type(tickets=tickets)

        notion_payload = LastTicketAnalysisPageBuilder(
            database_id=self._database_id,
            team_key=self._team_key,
            inspection_date=self._inspection_date,
            nb_tickets=nb_tickets,
            tickets_per_description=tickets_per_description_status,
            tickets_per_status=tickets_per_status,
            tickets_per_type=tickets_per_type
        ).build()

        self._notion_service.insert_notion_page(payload=notion_payload)

    @staticmethod
    def _bucket_tickets_per_description_status(tickets: list[Dict]) -> Dict:
        results = {}
        for ticket in tickets:
            if ticket['description'] is not None and len(ticket['description']) > 0:
                key = 'Description'
            else:
                key = 'No Description'

            if key in results.keys():
                results[key].append(ticket)
            else:
                results[key] = [ticket]

        return results

    @staticmethod
    def _bucket_tickets_per_type(tickets: list[Dict]) -> Dict:
        results = {}
        for ticket in tickets:
            if 'Bug' in [label['name'] for label in ticket['labels']['nodes']]:
                key = 'Bug'
            elif (ticket['project'] is not None and ticket['project']['name'] is not None and
                  ticket['project']['name'] in ['Payment Optimizations', 'Tech Improvements']):
                key = 'Tech Task'
            elif ticket['project'] is not None:
                key = 'Product Task with a project'
            else:
                key = 'Product Task without a project'

            if key in results.keys():
                results[key].append(ticket)
            else:
                results[key] = [ticket]

        return results
