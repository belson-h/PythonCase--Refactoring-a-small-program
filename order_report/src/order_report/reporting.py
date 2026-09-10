import pandas as pd

from order_report.transformation import calculate_return_rate

def build_overview(orders: pd.DataFrame) -> pd.DataFrame:
    """Sammanställer en översiktsrapport med totala nyckeltal för orderdatan."""
    total_sales = round(orders["discounted_value"].sum(), 2)
    order_count = orders["order_id"].nunique()
    return_count = int(orders["returned"].sum())

    return pd.DataFrame(
        {
        "metric": ["total_sales", "order_count","return_count"],
        "value": [total_sales, order_count, return_count],
        }
    )

# returns_by_category.csv kommer innehålla en total_sales-kolumn den inte hade i originalet, 
# vilket är en medveten designförenkling.

def summarize_by(
        orders: pd.DataFrame,
        group_column: str,
        sort_by: str = "total_sales",
        ascending: bool = False,
) -> pd.DataFrame:
    """ Sammanställer försäljning och returer grupperat på angiven kolumn. 

    Args: 
        orders: förebereder orderdata (efter prepare_order_data).
        group_column: kolumn att gruppera på, tex "product_category" eller "region".
        sort_by: kolumn att sortera resultatet efter (tex "total_sales" eller "return_rate").
        ascending: sorteringsordning.

    Returns: 
        En DataFrame med order_count, total_sales, returns och return_rate per grupp.
    """

    summary = orders.groupby(group_column, as_index=False).agg(
        order_count=("order_id", "nunique"),
        total_sales=("discounted_value", "sum"),
        returns=("returned", "sum")
    )

    summary["total_sales"] = summary["total_sales"].round(2)
    summary["return_rate"] = calculate_return_rate(
        summary["returns"], summary["order_count"]
    )

    return summary.sort_values(sort_by, ascending=ascending).reset_index(drop=True)