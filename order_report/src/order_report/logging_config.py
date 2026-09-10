import logging

def configure_logging() -> None:
    """Konfigurerar loggning centralt för hela programmet"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        )