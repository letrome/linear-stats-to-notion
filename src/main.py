from src.analysis_service.bug_analysis_service import BugAnalysisService
from src.analysis_service.cycle_analysis_service import CycleAnalysisService
from src.analysis_service.ticket_analysis_service import TicketAnalysisService
from src.properties import Properties

analysis_services = {
    "BUG": BugAnalysisService,
    "CYCLE": CycleAnalysisService,
    "TICKET": TicketAnalysisService
}


def main():
    properties = Properties()
    for mode in properties.mode:
        analysis_services[mode](properties=properties).run()


if __name__ == "__main__":
    main()
