import logging

from app.core.config import settings


logging.basicConfig(
    level=getattr(
        logging,
        settings.LOG_LEVEL.upper(),
        logging.INFO
    ),
    format=(
        "%(asctime)s - "
        "%(name)s - "
        "%(levelname)s - "
        "%(message)s"
    )
)


logger = logging.getLogger(
    "document_qa_assistant"
)