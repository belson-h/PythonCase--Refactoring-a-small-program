import pandas as pd
import logging

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {
        "order_id",
        "order_date",
        "customer_id",
        "region",
        "product_category",
        "quantity",
        "unit_price",
        "discount",
        "returned",
    }

def prepare_order_data(history: pd.DataFrame) -> pd.DataFrame:
    """Validerar att nödvändiga kolumner finns och rensar/normaliserar orderdata.
    
    Fyller saknade eller ogiltiga värden enligt fasta regler (tex median för pris).
    Kastar ValueError om obligatoriska kolumner saknas.

    Args: 
        orders: rå orderdata

    Returns:
        En ny DataFrame med rensade och normaliserade kolumner. 
    """
    missing_columns = REQUIRED_COLUMNS.difference(history.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Saknade kolumner: {missing}")

    prepared = history.copy()

    prepared["region"] = (
        prepared["region"].fillna("Unknown").astype(str).str.strip().str.title()
    )

    prepared["product_category"] = (
        prepared["product_category"]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .str.title()
        )

    missing_quantity = prepared["quantity"].isna().sum()
    prepared["quantity"] = pd.to_numeric(prepared["quantity"], errors="coerce").fillna(1)
    if missing_quantity:
        logger.warning("Fyllde i %d saknade quantity-värden med 1", missing_quantity)

    prepared["unit_price"] = pd.to_numeric(prepared["unit_price"], errors="coerce")
    missing_price = prepared["unit_price"].isna().sum()
    prepared["unit_price"] = prepared["unit_price"].fillna(prepared["unit_price"].median())
    if missing_price:
        logger.warning("Fyllde i %d saknade unit_price-värden med medianvärdet", missing_price)

    missing_discount = prepared["discount"].isna().sum()
    prepared["discount"] = pd.to_numeric(prepared["discount"], errors="coerce").fillna(0)
    if missing_discount:
        logger.warning("Fyllde i %d saknade discount-värden med 0", missing_discount)
    
    prepared["returned"] = (
            prepared["returned"]
            .fillna("false")
            .astype(str)
            .str.strip()
            .str.lower()
            .isin(["true", "yes", "1", "ja"])
        )

    logger.info("Förberedde %d rader orderdata", len(prepared))

    return prepared