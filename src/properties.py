import argparse
from typing import Optional

from jproperties import Properties as JProperties

class Properties:
    def __init__(self):
        argument_parser = self.InnerArgumentParser()
        properties_file_path = self._validate_str(value=argument_parser.properties_file_path)
        properties = self._load_file(properties_file_path=properties_file_path)

        self._linear_api_key = self._validate_str(value=properties.get("linear_api_key").data)
        self._notion_api_key = self._validate_str(value=properties.get("notion_api_key").data)
        self._team_key = self._validate_str(value=properties.get("team_key").data)
        self._mode = self._validate_list_str(value=argument_parser.mode)
        if 'TICKET' in self._mode:
            self._ticket_analysis_db_id = self._validate_str(properties.get("ticket_analysis_db_id").data)
            self._linear_ticket_request_template = self._validate_str(
                properties.get("linear_ticket_request_template").data)
        else:
            self._ticket_analysis_db_id = None
            self._linear_ticket_request_template = None
        if 'BUG' in self._mode:
            self._bug_analysis_db_id = self._validate_str(properties.get("bug_analysis_db_id").data)
            self._linear_bug_request_template = self._validate_str(properties.get("linear_bug_request_template").data)
        else:
            self._bug_analysis_db_id = None
            self._linear_bug_request_template = None
        if 'CYCLE' in self._mode:
            self._cycle_analysis_db_id = self._validate_str(properties.get("cycle_analysis_db_id").data)
            self._linear_cycle_request_template = self._validate_str(
                properties.get("linear_cycle_request_template").data)
        else:
            self._cycle_analysis_db_id = None
            self._linear_cycle_request_template = None
        if 'TICKET' in self._mode or 'BUG' in self._mode:
            self._max_nb_tickets_to_analyze = self._validate_int(value=argument_parser.max_nb_tickets_to_analyze)
        else:
            self._max_nb_tickets_to_analyze = None

    @property
    def linear_api_key(self) -> str:
        return self._linear_api_key

    @property
    def notion_api_key(self) -> str:
        return self._notion_api_key

    @property
    def team_key(self) -> str:
        return self._team_key

    @property
    def mode(self) -> list[str]:
        return self._mode

    @property
    def cycle_analysis_db_id(self) -> Optional[str]:
        return self._cycle_analysis_db_id

    @property
    def bug_analysis_db_id(self) -> Optional[str]:
        return self._bug_analysis_db_id

    @property
    def ticket_analysis_db_id(self) -> Optional[str]:
        return self._ticket_analysis_db_id

    @property
    def max_nb_tickets_to_analyze(self) -> Optional[int]:
        return self._max_nb_tickets_to_analyze

    @property
    def linear_ticket_request_template(self) -> Optional[str]:
        return self._linear_ticket_request_template

    @property
    def linear_bug_request_template(self) -> Optional[str]:
        return self._linear_bug_request_template

    @property
    def linear_cycle_request_template(self) -> Optional[str]:
        return self._linear_cycle_request_template

    @staticmethod
    def _load_file(properties_file_path: str) -> JProperties:
        props = JProperties()
        with open(properties_file_path, 'rb') as properties_file:
            props.load(properties_file)

        return props

    @staticmethod
    def _validate_str(value: str) -> str:
        assert value is not None
        value = str(value)
        assert len(value) > 0
        return value

    @staticmethod
    def _validate_list_str(value: list[str]) -> list[str]:
        value = list(value)
        assert len(value) > 0
        return [Properties._validate_str(item) for item in value]

    @staticmethod
    def _validate_int(value: int) -> int:
        value = int(value)
        assert value > 0
        return value

    class InnerArgumentParser:
        def __init__(self):
            parser = argparse.ArgumentParser(description="Linear stats to Notion")
            parser.add_argument(
                '--properties-file-path',
                dest='properties_file_path',
                type=str,
                default="/resources/configuration.properties"
            )

            parser.add_argument(
                '--max-nb-tickets-to-analyze',
                dest='max_nb_tickets_to_analyze',
                type=int,
                default=100
            )

            parser.add_argument(
                '-m', '--mode',
                dest='mode',
                nargs='+',
                type=str,
                help='list of modes, among \'TICKET\', \'BUG\' AND \'CYCLE\'',
                choices=['TICKET', 'BUG', 'CYCLE'],
                required=True
            )

            args = parser.parse_args()
            self._properties_file_path = args.properties_file_path
            self._mode = args.mode
            self._max_nb_tickets_to_analyze = args.max_nb_tickets_to_analyze

        @property
        def properties_file_path(self) -> str:
            return self._properties_file_path

        @property
        def mode(self) -> list[str]:
            return self._mode

        @property
        def max_nb_tickets_to_analyze(self) -> int:
            return self._max_nb_tickets_to_analyze
