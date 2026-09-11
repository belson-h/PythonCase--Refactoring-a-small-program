import pandas as pd

from order_report.transformation import(
    calculate_order_value,
    calculate_discount_value,
    calculate_return_rate,
    add_value_columns,
)


def test_calculate_order_value_normal_case():
    quantity = pd.Series([2, 3, 1])
    unit_price = pd.Series([100.0, 50.0, 20.0])

    result = calculate_order_value(quantity, unit_price)

    expected = pd.Series([200.0, 150.0, 20.0])
    pd.testing.assert_series_equal(result, expected)


def test_calculate_discounted_value_normal_case():
    order_value = pd.Series([200.0, 150.0, 100.0])
    discount = pd.Series([0.10, 0.20, 0.0])

    result = calculate_discount_value(order_value, discount)

    expected = pd.Series([180.0, 120.0, 100.0])
    pd.testing.assert_series_equal(result, expected)


def test_calculate_return_rate_normal_case():
    returns = pd.Series([2, 0, 1])
    order_count = pd.Series([4, 5, 2])

    result = calculate_return_rate(returns, order_count)

    expected = pd.Series([0.5, 0.0, 0.5])
    pd.testing.assert_series_equal(result, expected)


def test_add_value_columns_normal_case():
    orders = pd.DataFrame(
        {
            "quantity": [2, 1],
            "unit_price": [100.0, 50.0],
            "discount": [0.1, 0.0]
        }
    )

    result = add_value_columns(orders)

    expected_order_value = pd.Series([200.0, 50.0], name="order_value")
    expected_discounted_value = pd.Series([180.0, 50.0], name="discounted_value")

    pd.testing.assert_series_equal(result["order_value"], expected_order_value)
    pd.testing.assert_series_equal(result["discounted_value"], expected_discounted_value)

