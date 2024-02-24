from typing import Dict, Optional

from src.http_client import HttpClient
from src.linear.graphql_request import GraphqlRequest

LINEAR_URL = "https://api.linear.app/graphql"


class LinearService:
    def __init__(self, api_key: str, team_key: str, linear_cycle_request_template: Optional[str] = None,
                 linear_ticket_request_template: Optional[str] = None,
                 linear_bug_request_template: Optional[str] = None):
        headers = {
            'Content-Type': "application/json",
            'Authorization': api_key
        }
        self._http_client = HttpClient(headers=headers)
        self._team_key = team_key
        self._graphql_request = GraphqlRequest(linear_cycle_request_template=linear_cycle_request_template,
                                               linear_ticket_request_template=linear_ticket_request_template,
                                               linear_bug_request_template=linear_bug_request_template)

    def get_last_tickets(self, max_nb_tickets: int) -> Dict:
        payload = self._graphql_request.build_linear_ticket_request(team_key=self._team_key,
                                                                    max_nb_tickets=max_nb_tickets)

        return self._http_client.post(url=LINEAR_URL, payload=payload, response_json_path=['data', 'issues', 'nodes'])

    def get_last_bugs(self, max_nb_tickets: int) -> Dict:
        payload = self._graphql_request.build_linear_bug_request(team_key=self._team_key,
                                                                 max_nb_tickets=max_nb_tickets)

        return self._http_client.post(url=LINEAR_URL, payload=payload, response_json_path=['data', 'issues', 'nodes'])

    def get_cycle_data(self):
        payload = self._graphql_request.build_linear_cycle_request(team_key=self._team_key)

        return self._http_client.post(url=LINEAR_URL, payload=payload, response_json_path=['data', 'cycles', 'nodes'])
