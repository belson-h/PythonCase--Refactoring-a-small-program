import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def load_orders(input_path: Path) -> pd.DataFrame:
    """Läser in orderdata från CSV-fil"""
    orders = pd.read_csv(input_path)
    logger.info("Läste in %d rader från %s", len(orders), input_path)
    return orders

def save_report(data: pd.DataFrame, output_dir: Path, filename: str) -> Path:
    """Sparar en DataFrame som CSV i output_dir och returnerar filens sökväg."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    data.to_csv(output_path, index=False)
    logger.info("Sparade %s (%d rader)", output_path, len(data))
    return output_path