import datetime
import structlog


def timestamper(_, __, event_dict):
    event_dict["time"] = datetime.datetime.now().isoformat()
    return event_dict


structlog.configure(processors=[timestamper, structlog.dev.ConsoleRenderer()])
logger = structlog.get_logger()
