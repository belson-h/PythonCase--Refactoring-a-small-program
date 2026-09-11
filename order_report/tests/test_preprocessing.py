import pandas as pd
import pytest

from order_report.preprocessing import prepare_order_data

def _make_valid_orders(**overrides) -> pd.DataFrame:
    """Hjälpfunktion som bygger en minimal orderdata-DataFrame, 
    istället för att bygga upp en ny DataFrame från grunden i varje test.
    overrides låter enskilda tester skriva över specifika kolumner."""
    data = {
        "order_id": [1, 2],
        "order_date": ["2026-08-01", "2026-08-02"],
        "customer_id":[10, 11],
        "region": ["north", None],
        "product_category": ["home", "Sports"],
        "quantity": [2, None],
        "unit_price": [100.0, None],
        "discount": [0.1, None],
        "returned": ["true", None],
    }
    data.update(overrides)
    return pd.DataFrame(data)


def test_prepare_order_data_normal_case():
    orders = _make_valid_orders()

    result = prepare_order_data(orders)

    assert result["region"].tolist() == ["North", "Unknown"]
    assert result["product_category"].tolist() == ["Home", "Sports"]
    assert result["quantity"].tolist() == [2, 1]
    assert result["discount"].tolist() == [0.1, 0.0]
    assert result["returned"].tolist() == [True, False]


def test_prepare_order_data_missing_required_column_raises_error():
    """Edge case: en obligatorisk kolumn saknas helt."""
    orders = _make_valid_orders().drop(columns=["region"])

    with pytest.raises(ValueError, match="region"):
        prepare_order_data(orders)


def test_prepare_order_data_empty_dataframe():
    """Edge case: tom DataFrame (0 rader) men med rätt kolumner."""
    empty_orders = _make_valid_orders().iloc[0:0]

    result = prepare_order_data(empty_orders)

    assert len(result) == 0
    assert list(result.columns) == list(empty_orders.columns)