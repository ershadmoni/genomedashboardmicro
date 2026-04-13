import logging
import sys
from typing import Optional

from app.core.config import get_settings


def setup_logging(level: Optional[str] = None) -> None:
    """
    Configure global logging.

    Features:
    - Structured format
    - Console output (stdout)
    - Configurable log level
    """

    settings = get_settings()
    log_level = (level or settings.LOG_LEVEL).upper()

    logging.basicConfig(
        level=log_level,
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def get_logger(name: str) -> logging.Logger:
    """
    Create module-level logger.
    """
    return logging.getLogger(name)
