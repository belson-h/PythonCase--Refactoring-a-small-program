import logging
import sys

from order_report.config import ReportConfig
from order_report.logging_config import configure_logging
from order_report.pipeline import run

logger = logging.getLogger(__name__)


def main() -> None:
    configure_logging()
    config = ReportConfig()

    try:
        run(config)
    except FileNotFoundError:
        logger.error("Hittade inte indatafilen: %s", config.input_path)
        sys.exit(1)
    except ValueError as error:
        logger.error("Ogiltig data: %s", error)
        sys.exit(1)


if __name__ == "__main__":
    main()