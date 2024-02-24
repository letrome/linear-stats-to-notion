from datetime import datetime
from typing import Dict

from src.notion.document_builder import DocumentBuilder

COVER_URL = "https://images.unsplash.com/photo-1593510987185-1ec2256148a3"
ICON = "🔎"


class CycleAnalysisPageBuilder(DocumentBuilder):
    def __init__(self, database_id: str, team_key: str, inspection_date: datetime, cycle_name: str,
                 cycle_data: Dict):
        super().__init__(icon=ICON, cover_url=COVER_URL, database_id=database_id, team_key=team_key,
                         inspection_date=inspection_date,
                         title=team_key + " - " + cycle_name,
                         generation_method="automated")

        self._cycle_name = cycle_name
        self._cycle_data = cycle_data

    def _properties_block(self) -> Dict:
        return {
            'properties': {
                "Nom": self._title_block(self._title),
                "Cycle": self._rich_text_block(value=self._cycle_name),
                "generation method": self._select_block(value=self._generation_method),
                "Date of inspection": self._date_block(self._inspection_date)
            }
        }

    def _children_block(self) -> Dict:
        children = []
        children.extend(self._iteration_summary_blocks(self._cycle_data))
        children.append(self._divider_block())
        children.extend(self._iteration_evolution_blocks(self._cycle_data))
        children.append(self._divider_block())
        children.extend(self._ticket_details_blocks("Details of the uncompleted tickets",
                                                    self._cycle_data['uncompletedIssuesUponClose']['nodes']))

        return {
            'children': children[:100]
        }

    def _iteration_summary_blocks(self, iteration_data: Dict):
        children = [
            self._h1_block("Summary"),
            self._paragraph_with_bold_key_block("Date of beginning. ", iteration_data['startsAt']),
            self._paragraph_with_bold_key_block("Date of end. ", iteration_data['endsAt']),
            self._paragraph_with_bold_key_block("Max nb of tickets in the cycle. ",
                                                str(max(iteration_data['scopeHistory'])))
        ]
        scope_added = 0
        scope_removed = 0
        previous_hist = -1
        for hist in iteration_data['scopeHistory']:
            if previous_hist >= 0:
                if hist > previous_hist:
                    scope_added += hist - previous_hist
                else:
                    scope_removed += previous_hist - hist
            previous_hist = hist
        children.append(self._paragraph_with_bold_key_block("Tickets added after the beginning. ", str(scope_added)))
        children.append(
            self._paragraph_with_bold_key_block("Tickets removed after the beginning. ", str(scope_removed)))
        children.append(self._paragraph_with_bold_key_block("Nb of completed tickets. ",
                                                            str(iteration_data['completedScopeHistory'][-1])))
        children.append(self._paragraph_with_bold_key_block("Progress score. ",
                                                            "{:.4f}".format(round(iteration_data['progress'], 4))))
        return children

    def _iteration_evolution_blocks(self, iteration_data: Dict):
        return [
            self._h1_block("History over time"),
            self._h2_block("Evolution of the nb of tickets in the iteration over time"),
            self._xychart_block("nb tickets over time", iteration_data["scopeHistory"]),
            self._h2_block("Evolution of the nb of tickets in progress in the iteration over time"),
            self._xychart_block("nb tickets in progress over time", iteration_data["inProgressScopeHistory"]),
            self._h2_block("Evolution of the nb of tickets resolved in the iteration over time"),
            self._xychart_block("nb tickets completed over time", iteration_data["completedScopeHistory"])
        ]
