import pandas as pd

def calculate_order_value(quantity: pd.Series, unit_price: pd.Series) -> pd.Series:
    """Berknar ordervärde som quantity * unit_price."""
    return quantity * unit_price

def calculate_discount_value(order_value: pd.Series, discount: pd.Series) -> pd.Series:
    """Beräknar ordervärde efter rabatt."""
    return order_value * (1 - discount)

def add_value_columns(orders: pd.DataFrame) -> pd.DataFrame:
    """Lägger till order_value och discount_value som nya kolumner."""
    result = orders.copy()
    result["order_value"] = calculate_order_value(result["quantity"], result["unit_price"])
    result["discounted_value"] = calculate_discount_value(
        result["order_value"], result["discount"]
    )
    return result

def calculate_return_rate(returns: pd.Series, order_count: pd.Series) -> pd.Series:
    """Beräknar andel returer som returns / order_count.
    
        Ger NaN där order_count är 0, istället för att kasta ett fel.
    """
    return (returns / order_count).round(3)

