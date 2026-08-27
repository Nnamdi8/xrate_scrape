import sys
from datetime import datetime, timedelta

import yahoo_fin.stock_info as si # type: ignore



def convert_currency_yahoofin(src, dst, amount):
    # Yahoo Finance currency pair format, e.g. USDNGN=X
    symbol = f"{src.upper()}{dst.upper()}=X"

    # Get recent data
    latest_data = si.get_data(
        symbol,
        interval="1m",
        start_date=datetime.now() - timedelta(days=1)
    )

    if latest_data.empty:
        raise ValueError(f"No data found for currency pair: {symbol}")

    # Get the latest datetime
    last_updated_datetime = latest_data.index[-1].to_pydatetime()

    # Get the latest exchange rate
    latest_price = latest_data.iloc[-1]["close"]

    # Convert the amount
    converted_amount = latest_price * amount

    return last_updated_datetime, converted_amount


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python currency.py SOURCE DESTINATION AMOUNT")
        print("Example: python currency.py USD NGN 100")
        sys.exit(1)

    source_currency = sys.argv[1]
    destination_currency = sys.argv[2]

    try:
        amount = float(sys.argv[3])
    except ValueError:
        print("Error: Amount must be a number.")
        sys.exit(1)

    try:
        last_updated_datetime, exchange_rate = convert_currency_yahoofin(
            source_currency,
            destination_currency,
            amount
        )

        print("Last updated datetime:", last_updated_datetime)
        print(
            f"{amount} {source_currency.upper()} = "
            f"{exchange_rate:.2f} {destination_currency.upper()}"
        )

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)