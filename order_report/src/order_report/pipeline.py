import logging
import pandas as pd

from order_report.config import ReportConfig
from order_report.io_utils import load_orders, save_report
from order_report.preprocessing import prepare_order_data
from order_report.transformation import add_value_columns
from order_report.reporting import build_overview, summarize_by

logger = logging.getLogger(__name__)

def run(config: ReportConfig) -> None:
    """Kör hela orderrapport-flödet: läs, förbered, beräkna, sammanställ och spara"""

    orders = load_orders(config.input_path)
    prepared = prepare_order_data(orders)
    prepared = add_value_columns(prepared)

    overview = build_overview(prepared)
    sales_by_category = summarize_by(prepared, "product_category", sort_by="total_sales")
    sales_by_region = summarize_by(prepared, "region", sort_by="total_sales")
    returns_by_category = summarize_by(prepared, "product_category", sort_by="return_rate")

    save_report(overview, config.output_dir, "overview.csv")
    save_report(sales_by_category, config.output_dir, "sales_by_category.csv")
    save_report(sales_by_region, config.output_dir, "sales_by_region.csv")
    save_report(returns_by_category, config.output_dir, "returns_by_category.csv")

    logger.info("Klart")