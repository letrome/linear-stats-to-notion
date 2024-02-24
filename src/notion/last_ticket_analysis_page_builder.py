from datetime import datetime
from typing import Dict, List

from src.notion.document_builder import DocumentBuilder

COVER_URL = "https://images.unsplash.com/photo-1593510987185-1ec2256148a3"
ICON = "🔎"

COLOR_PER_DESCRIPTION = {
    "No Description": {
        "name": "red",
        "hex": "#C4554D"
    },
    "Description": {
        "name": "blue",
        "hex": "#487CA5"
    }
}
COLOR_PER_TYPE = {
    "Bug": {
        "name": "red",
        "hex": "#C4554D"
    },
    "Tech Task": {
        "name": "yellow",
        "hex": "#C29343"
    },
    "Product Task with a project": {
        "name": "blue",
        "hex": "#487CA5"
    },
    "Product Task without a project": {
        "name": "green",
        "hex": "#548164"
    }
}


class LastTicketAnalysisPageBuilder(DocumentBuilder):
    def __init__(self, database_id: str, team_key: str, inspection_date: datetime, nb_tickets: int,
                 tickets_per_description: Dict, tickets_per_status: Dict, tickets_per_type: Dict):
        super().__init__(icon=ICON, cover_url=COVER_URL, database_id=database_id, team_key=team_key,
                         inspection_date=inspection_date,
                         title=team_key + " - " + inspection_date.isoformat(sep='T', timespec='auto'),
                         generation_method="automated")

        self._nb_tickets = nb_tickets
        self._tickets_per_description = tickets_per_description
        self._tickets_per_status = tickets_per_status
        self._tickets_per_type = tickets_per_type

    def _properties_block(self) -> Dict:
        return {
            'properties': {
                "Nom": self._title_block(self._title),
                "nb_tickets": self._number_block(value=self._nb_tickets),
                "generation method": self._select_block(value=self._generation_method),
                "Date of inspection": self._date_block(self._inspection_date)
            }
        }

    def _children_block(self) -> Dict:
        children = []
        children.extend(self._description_blocks())
        children.append(self._divider_block())
        children.extend(self._status_blocks(tickets_per_status=self._tickets_per_status, nb_tickets=self._nb_tickets))
        children.append(self._divider_block())
        children.extend(self._type_blocks(tickets_per_type=self._tickets_per_type, nb_tickets=self._nb_tickets))

        return {
            'children': children
        }

    def _description_blocks(self) -> List:
        tickets_per_desc = self._tickets_per_description
        nb_tickets_with_description = self.nb_values_for_key(tickets_per_desc, 'Description')
        pie_colors = []
        pie_title = "Tickets with a description"
        pie_data = {}
        for desc in sorted(tickets_per_desc.keys(), key=lambda _desc: len(tickets_per_desc[_desc])):
            pie_colors.append(COLOR_PER_DESCRIPTION[desc]['hex'])
            pie_data[desc] = len(tickets_per_desc[desc])

        children = [
            self._h1_block("Ticket description"),
            self._paragraph_block(f"On {self._nb_tickets} tickets, {nb_tickets_with_description} have a description."),
            self._blank_line(),
            self._h2_block("Chart"),
            self._pie_chart_block(pie_colors, pie_title, pie_data),
            self._blank_line(),
            self._h2_block("List of tickets without description"),
        ]
        for ticket in tickets_per_desc['No Description']:
            children.append(self._bullet_with_link_block(ticket['identifier'], ticket['url']))
        children.append(self._blank_line())
        return children

    def _type_blocks(self, tickets_per_type: Dict, nb_tickets: int) -> List:

        children = [self._h1_block("Tickets type"),
                    self._paragraph_block(f"On {nb_tickets} tickets, their type are split in the following:")
                    ]
        pie_colors = []
        pie_title = "Tickets per type"
        pie_data = {}
        for t_type in sorted(tickets_per_type.keys(), key=lambda _type: len(tickets_per_type[_type])):
            children.append(self._colored_bullet_block(t_type, len(tickets_per_type[t_type]),
                                                       COLOR_PER_TYPE[t_type]['name']))
            pie_colors.append(COLOR_PER_TYPE[t_type]['hex'])
            pie_data[t_type] = len(tickets_per_type[t_type])
        children.append(self._blank_line())
        children.append(self._h2_block("Chart"))
        children.append(self._pie_chart_block(pie_colors, pie_title, pie_data))
        return children
