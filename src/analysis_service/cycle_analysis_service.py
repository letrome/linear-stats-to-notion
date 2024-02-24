from typing import Dict

from src.analysis_service.analysis_service import AnalysisService
from src.notion.cycle_analysis_page_builder import CycleAnalysisPageBuilder
from src.properties import Properties


class CycleAnalysisService(AnalysisService):
    def __init__(self, properties: Properties):
        super().__init__(
            linear_api_key=properties.linear_api_key,
            notion_api_key=properties.notion_api_key,
            team_key=properties.team_key,
            linear_ticket_request_template=properties.linear_ticket_request_template,
            linear_bug_request_template=properties.linear_bug_request_template,
            linear_cycle_request_template=properties.linear_cycle_request_template
        )

        self._database_id = properties.cycle_analysis_db_id

    def run(self) -> None:
        cycle_data = self._linear_service.get_cycle_data()
        cycle_data_by_name = self._bucket_cycle_data_by_name(cycle_data=cycle_data)

        for cycle_name in cycle_data_by_name.keys():
            if not self._notion_service.is_cycle_doc_exists(database_id=self._database_id, cycle_name=cycle_name):
                notion_payload = CycleAnalysisPageBuilder(
                    database_id=self._database_id,
                    team_key=self._team_key,
                    cycle_name=cycle_name,
                    inspection_date=self._inspection_date,
                    cycle_data=cycle_data_by_name[cycle_name]
                ).build()
                self._notion_service.insert_notion_page(payload=notion_payload)

    @staticmethod
    def _bucket_cycle_data_by_name(cycle_data: Dict) -> Dict:
        results = {}
        for item in cycle_data:
            results[item['name']] = item
        return results
