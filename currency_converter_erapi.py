import sys
import requests
from dateutil.parser import parse


def get_all_exchange_rates_erapi(src):
    # Construct the API URL
    url = f"https://open.er-api.com/v6/latest/{src}"

    # Request the ExchangeRate API
    response = requests.get(url)

    # Convert response to Python dictionary
    data = response.json()

    if data["result"] == "success":
        # Get the last updated datetime
        last_updated_datetime = parse(data["time_last_update_utc"])

        # Get all exchange rates
        exchange_rates = data["rates"]

        return last_updated_datetime, exchange_rates

    else:
        raise ValueError("Failed to get exchange rates")


def convert_currency_erapi(src, dst, amount):
    # Get all exchange rates
    last_updated_datetime, exchange_rates = get_all_exchange_rates_erapi(src)

    # Get the destination currency rate
    exchange_rate = exchange_rates[dst]

    # Convert the amount
    converted_amount = exchange_rate * amount

    return last_updated_datetime, converted_amount


if __name__ == "__main__":
    source_currency = sys.argv[1].upper()
    destination_currency = sys.argv[2].upper()
    amount = float(sys.argv[3])

    last_updated_datetime, exchange_rate = convert_currency_erapi(
        source_currency,
        destination_currency,
        amount
    )

    print("Last updated datetime:", last_updated_datetime)
    print(
        f"{amount} {source_currency} = "
        f"{exchange_rate:.2f} {destination_currency}"
    )

#RUN THE PROGRAM AS BELLOW
# python currency_converter_erapi.py USD NGN 100