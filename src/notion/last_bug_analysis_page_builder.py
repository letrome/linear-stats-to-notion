from datetime import datetime
from typing import Dict

from src.notion.document_builder import DocumentBuilder

COVER_URL = "https://images.unsplash.com/photo-1593510987185-1ec2256148a3"
ICON = "🔎"


class LastBugAnalysisPageBuilder(DocumentBuilder):
    def __init__(self, database_id: str, team_key: str, inspection_date: datetime, nb_tickets: int,
                 tickets_per_status: Dict, timedelta: Dict, last_10_tickets: list):
        super().__init__(icon=ICON, cover_url=COVER_URL, database_id=database_id, team_key=team_key,
                         inspection_date=inspection_date,
                         title=team_key + " - " + inspection_date.isoformat(sep='T', timespec='auto'),
                         generation_method="automated")

        self._nb_tickets = nb_tickets
        self._tickets_per_status = tickets_per_status
        self._timedelta = timedelta
        self._last_10_tickets = last_10_tickets

    def _properties_block(self) -> Dict:
        return {
            'properties': {
                "Name": self._title_block(self._title),
                "Nb Tickets": self._number_block(value=self._nb_tickets),
                "Generation Method": self._select_block(value=self._generation_method),
                "Date of Inspection": self._date_block(self._inspection_date)
            }
        }

    def _children_block(self) -> Dict:
        children = []

        children.extend(self._status_blocks(tickets_per_status=self._tickets_per_status, nb_tickets=self._nb_tickets))
        children.append(self._divider_block())
        children.extend(self._resolution_time_blocks())
        children.append(self._divider_block())
        children.extend(
            self._ticket_details_blocks(f"Last {len(self._last_10_tickets)} bugs synthesis", self._last_10_tickets))

        return {
            "children": children
        }

    def _resolution_time_blocks(self) -> list:
        timedelta = self._timedelta
        children = [
            self._h1_block("Resolution time"),
            self._blank_line(),
            self._paragraph_block(f"On the {self._nb_tickets} bug tickets analyzed:")
        ]

        cr_st_value = int(timedelta['delta_created_started']['value_hours'])
        cr_st_size = int(timedelta['delta_created_started']['sample_size'])
        children.append(self._bullet_block(
            f"The average time between a ticket creation and the beginning of the work is {cr_st_value}hours."))
        children.append(self._gray_italic_paragraph_block(f"(computation made on {cr_st_size} tickets)"))
        children.append(self._blank_line())

        st_cp_value = int(timedelta['delta_started_completed']['value_hours'])
        st_cp_size = int(timedelta['delta_started_completed']['sample_size'])
        children.append(
            self._bullet_block(f"The average time between a ticket start and its resolution is {st_cp_value}hours."))
        children.append(self._gray_italic_paragraph_block(f"(computation made on {st_cp_size} tickets)"))
        children.append(self._blank_line())

        cr_cp_value = int(timedelta['delta_created_completed']['value_hours'])
        cr_cp_size = int(timedelta['delta_created_completed']['sample_size'])
        children.append(
            self._bullet_block(f"The average time between a ticket creation and its resolution is {cr_cp_value}hours."))
        children.append(self._gray_italic_paragraph_block(f"(computation made on {cr_cp_size} tickets)"))
        children.append(self._blank_line())

        children.append(self._h2_block("Chart"))
        title = "average time between creation, dev and resolution (in hours)"

        gantt_items = [
            {
                "label": "creation -> resolution",
                "duration": cr_cp_value,
                "begin": 0,
                "end": cr_cp_value
            },
            {
                "label": "creation -> work start",
                "duration": cr_st_value,
                "begin": 0,
                "end": cr_st_value
            },
            {
                "label": "work start -> resolution",
                "duration": st_cp_value,
                "begin": cr_st_value,
                "end": cr_cp_value
            }
        ]
        children.append(self._gantt_diagram_block(title, "%H", gantt_items))
        return children
