import sys
import requests
from bs4 import BeautifulSoup as bs
from dateutil.parser import parse
from pprint import pprint


def get_exchange_list(currency, amount=1):
    """Get exchange rates from X-Rates."""

    url = f"https://www.x-rates.com/table/?from={currency}&amount={amount}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    # Initialize BeautifulSoup
    soup = bs(response.content, "html.parser")

    # Get the last updated time
    timestamp = soup.find("span", class_="ratesTimestamp")

    if timestamp:
        price_datetime = parse(timestamp.get_text(strip=True))
    else:
        price_datetime = None

    # Get the exchange rate tables
    exchange_tables = soup.find_all("table")

    exchange_rates = {}

    for exchange_table in exchange_tables:
        for tr in exchange_table.find_all("tr"):
            tds = tr.find_all("td")

            if len(tds) >= 2:
                target_currency = tds[0].get_text(strip=True)

                try:
                    exchange_rate = float(
                        tds[1].get_text(strip=True).replace(",", "")
                    )
                    exchange_rates[target_currency] = exchange_rate
                except ValueError:
                    continue

    return price_datetime, exchange_rates


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python exchange.py USD [amount]")
        sys.exit(1)

    source_currency = sys.argv[1].upper()

    amount = 1
    if len(sys.argv) >= 3:
        amount = float(sys.argv[2])

    price_datetime, exchange_rates = get_exchange_list(
        source_currency, amount
    )

    print("Last updated:", price_datetime)
    pprint(exchange_rates)