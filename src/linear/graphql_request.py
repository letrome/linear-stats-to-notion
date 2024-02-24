import json
from typing import Optional, Dict

from jinja2 import Environment, FileSystemLoader, select_autoescape, Template


class GraphqlRequest:
    def __init__(self, linear_cycle_request_template: Optional[str],
                 linear_ticket_request_template: Optional[str],
                 linear_bug_request_template: Optional[str]):
        self._linear_ticket_request_template = linear_ticket_request_template
        self._linear_cycle_request_template = linear_cycle_request_template
        self._linear_bug_request_template = linear_bug_request_template

        self._env = Environment(loader=FileSystemLoader("resources"), autoescape=select_autoescape())

    def build_linear_ticket_request(self, team_key: str, max_nb_tickets: int) -> Dict:
        template = self._load_template(self._linear_ticket_request_template)
        return json.loads(template.render({
            "team_key": team_key,
            "max_nb_tickets": max_nb_tickets
        }))

    def build_linear_bug_request(self, team_key: str, max_nb_tickets: int) -> Dict:
        template = self._load_template(self._linear_bug_request_template)
        return json.loads(template.render({
            "team_key": team_key,
            "max_nb_tickets": max_nb_tickets
        }))

    def build_linear_cycle_request(self, team_key: str) -> Dict:
        template = self._load_template(self._linear_cycle_request_template)
        return json.loads(template.render({
            "team_key": team_key
        }))

    def _load_template(self, filepath: str) -> Template:
        return self._env.get_template(filepath)
