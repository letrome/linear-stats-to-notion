from abc import abstractmethod
from datetime import datetime
from typing import Dict, List

SIMPLIFIED_COLOR_PER_STATUS = {
    'To Do': {
        "hex": "#487CA5"
    },
    'Dev': {
        "hex": "#C29343"
    },
    'Review': {
        "hex": "#B65C8D"
    },
    'Done': {
        "hex": "#548164"
    },
    'Canceled': {
        "hex": "#C4554D"
    }
}
COLOR_PER_STATUS = {
    "Ready to Dev": {
        "name": "blue",
        "hex": "#487CA5"
    },
    "Completed": {
        "name": "green",
        "hex": "#548164"
    },
    "Ready to Go-Live": {
        "name": "purple",
        "hex": "#8A67AB"
    },
    "Canceled": {
        "name": "red",
        "hex": "#C4554D"
    },
    "Dev": {
        "name": "yellow",
        "hex": "#C29343"
    },
    "Dev Review": {
        "name": "pink",
        "hex": "#B65C8D"
    },
    "Backlog": {
        "name": "gray",
        "hex": "#787774"
    },
    "Feedback": {
        "name": "brown",
        "hex": "#986E58"
    },
    "Product Review": {
        "name": "orange",
        "hex": "#CC782F"
    },
}


class DocumentBuilder:
    def __init__(self, icon: str, cover_url: str, database_id: str, team_key: str, inspection_date: datetime,
                 title: str, generation_method: str):
        self._icon = icon
        self._cover_url = cover_url
        self._database_id = database_id
        self._team_key = team_key
        self._inspection_date = inspection_date
        self._title = title
        self._generation_method = generation_method

    def build(self) -> Dict:
        return (self._parent_block() | self._icon_block() | self._cover_block() | self._properties_block() |
                self._children_block())

    def _parent_block(self):
        return {
            "parent": {
                "database_id": self._database_id
            }
        }

    def _icon_block(self):
        return {
            "icon": {
                "emoji": self._icon
            }
        }

    def _cover_block(self):
        return {
            "cover": {
                "external": {
                    "url": self._cover_url
                }
            }
        }

    @abstractmethod
    def _properties_block(self) -> Dict:
        pass

    @abstractmethod
    def _children_block(self) -> Dict:
        pass

    def _ticket_details_blocks(self, title, ticket_list: List):
        children = [
            self._h1_block(title),
            self._blank_line()
        ]
        for ticket in ticket_list:
            children.append(self._h2_with_link_block(ticket["identifier"], ticket["url"], " - " + ticket["title"]))
            children.append(self._paragraph_with_bold_key_block("Status. ", ticket['state']['name']))
            if 'createdAt' in ticket.keys() and ticket['createdAt'] is not None:
                children.append(self._paragraph_with_bold_key_block("Creation Date. ", ticket['createdAt']))
            if 'startedAt' in ticket.keys() and ticket['startedAt'] is not None:
                children.append(self._paragraph_with_bold_key_block("Start Date. ", ticket['startedAt']))
            if 'completedAt' in ticket.keys() and ticket['completedAt'] is not None:
                children.append(self._paragraph_with_bold_key_block("Resolution Date. ", ticket['completedAt']))
            children.append(self._blank_line())

        return children

    def _status_blocks(self, tickets_per_status: Dict, nb_tickets: int) -> List:

        children = [
            self._h1_block("Ticket status"),
            self._paragraph_block(f"On {nb_tickets} tickets, their status are split in the following:")
        ]
        pie_colors = []
        pie_title = "tickets per status (exhaustive)"
        pie_data = {}
        for stat in sorted(tickets_per_status.keys(), key=lambda _stat: len(tickets_per_status[_stat])):
            pie_colors.append(COLOR_PER_STATUS[stat]['hex'])
            pie_data[stat] = len(tickets_per_status[stat])
            children.append(
                self._colored_bullet_block(stat, len(tickets_per_status[stat]), COLOR_PER_STATUS[stat]['name']))
        children.append(self._blank_line())
        children.append(self._h2_block("Exhaustive chart"))
        children.append(self._pie_chart_block(pie_colors, pie_title, pie_data))
        children.append(self._blank_line())
        children.append(self._h2_block("Simplified chart"))

        pie_colors = []
        pie_title = "tickets per status (simplified)"
        pie_data = {
            'To Do': self.nb_values_for_key(tickets_per_status, 'Backlog') + self.nb_values_for_key(tickets_per_status,
                                                                                                    'Ready to Dev'),
            'Dev': self.nb_values_for_key(tickets_per_status, 'Dev'),
            'Review': self.nb_values_for_key(tickets_per_status, 'Dev Review') + self.nb_values_for_key(
                tickets_per_status, 'Product Review') + self.nb_values_for_key(tickets_per_status, 'Feedback'),
            'Done': self.nb_values_for_key(tickets_per_status, 'Ready to Go-Live') + self.nb_values_for_key(
                tickets_per_status, 'Completed'),
            'Canceled': self.nb_values_for_key(tickets_per_status, 'Canceled')
        }
        for stat in sorted(pie_data.keys(), key=lambda _stat: pie_data[_stat]):
            pie_colors.append(SIMPLIFIED_COLOR_PER_STATUS[stat]['hex'])

        children.append(self._pie_chart_block(pie_colors, pie_title, pie_data))
        children.append(self._blank_line())

        return children

    @staticmethod
    def _title_block(value: str) -> Dict:
        return {
            "title": [
                {
                    "text": {
                        "content": value
                    }
                }
            ]
        }

    @staticmethod
    def _number_block(value: int) -> Dict:
        return {
            "number": value
        }

    @staticmethod
    def _select_block(value: str) -> Dict:
        return {
            "select": {
                "name": value
            }
        }

    @staticmethod
    def _date_block(value: datetime) -> Dict:
        return {
            "date": {
                "start": value.isoformat(sep='T', timespec='auto')
            }
        }

    @staticmethod
    def _rich_text_block(value: str) -> Dict:
        return {"rich_text": [{
            "type": "text",
            "text": {
                "content": value
            }
        }]}

    @staticmethod
    def _h1_block(text: str):
        return {
            "type": "heading_1",
            "heading_1": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": text
                        }
                    }
                ]
            }
        }

    @staticmethod
    def _h2_block(text: str):
        return {
            "type": "heading_2",
            "heading_2": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": text
                        }
                    }
                ]
            }
        }

    @staticmethod
    def _h2_with_link_block(text_with_link, link, text_without_link):
        return {
            "type": "heading_2",
            "heading_2": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": text_with_link,
                            "link": {
                                "url": link
                            }
                        }
                    },
                    {
                        "type": "text",
                        "text": {
                            "content": text_without_link
                        }
                    }
                ]
            }
        }

    @staticmethod
    def _paragraph_block(text: str):
        return {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": text
                        }
                    }
                ]
            }
        }

    @staticmethod
    def _paragraph_with_bold_key_block(bold_key, text):
        return {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": bold_key + ""
                        },
                        "annotations": {
                            "bold": True
                        }
                    },
                    {
                        "type": "text",
                        "text": {
                            "content": text
                        }
                    }
                ]
            }
        }

    @staticmethod
    def _gray_italic_paragraph_block(text):
        return {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": text
                        },
                        "annotations": {
                            "italic": True,
                            "color": "gray"
                        }
                    }
                ]
            }
        }

    @staticmethod
    def _blank_line():
        return {
            "type": "paragraph",
            "paragraph": {
                "rich_text": []
            }
        }

    @staticmethod
    def _divider_block():
        return {
            "type": "divider",
            "divider": {}
        }

    @staticmethod
    def _bullet_with_link_block(identifier, link):
        return {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": identifier,
                            "link": {
                                "url": link
                            }
                        }
                    }
                ]
            }
        }

    @staticmethod
    def _colored_bullet_block(status, nb_tickets, color):
        return {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": status + '.'
                        },
                        "annotations": {
                            "bold": True,
                            "color": color
                        }
                    },
                    {
                        "type": "text",
                        "text": {
                            "content": " " + str(nb_tickets)
                        }
                    }
                ]
            }
        }

    @staticmethod
    def _bullet_block(text):
        return {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": text
                        }
                    }
                ]
            }
        }

    @staticmethod
    def _pie_chart_block(pie_chart_colors: List, title: str, key_values: Dict):
        str_colors = ",".join([f"'pie{i + 1}': '{pie_chart_colors[i]}'" for i in range(len(pie_chart_colors))])
        str_data = "\n".join(f"\"{key}\": {key_values[key]}" for key in key_values.keys())
        text = f"""%%{{init: {{'theme': 'base', 'themeVariables': {{{str_colors}}}}}}}%%
        pie showData
            title {title}
            {str_data}
        """

        return {
            "type": "code",
            "code": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": text
                        }
                    }
                ],
                "language": "mermaid"
            }
        }

    @staticmethod
    def _gantt_diagram_block(title, axis_format, items: list):
        str_data = ""
        for item in items:
            str_data += f"section {item["label"]}\n{item["duration"]}   : {item["begin"]}, {item["end"]}\n"
        text = f"""
                gantt
                title {title}
                dateFormat X
                axisFormat {axis_format}
                {str_data}
    """

        return {
            "type": "code",
            "code": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": text
                        }
                    }
                ],
                "language": "mermaid"
            }
        }

    @staticmethod
    def _xychart_block(title, history_values):
        x_axis_labels = ','.join(f"d{i}" for i in range(len(history_values)))
        y_axis_labels = f"\"nb_tickets\" 0 --> {max(history_values)}"
        text = f"""
        xychart-beta
    title "{title}"
    x-axis [{x_axis_labels}]
    y-axis {y_axis_labels}
    bar {history_values}
        """

        return {
            "type": "code",
            "code": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": text
                        }
                    }
                ],
                "language": "mermaid"
            }
        }

    @staticmethod
    def nb_values_for_key(dct: Dict, key: str) -> 0:
        if key in dct:
            return len(dct[key])
        return 0
