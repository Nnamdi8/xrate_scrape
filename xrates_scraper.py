import argparse
import csv
import json
import time
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.x-rates.com/table/"


def scrape_xrates(source_currency, amount=1.0, retries=3):
    """Scrape exchange rates from X-Rates."""

    source_currency = source_currency.upper()

    params = {
        "from": source_currency,
        "amount": amount,
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/139 Safari/537.36"
        )
    }

    last_error = None

    for attempt in range(retries):
        try:
            response = requests.get(
                BASE_URL,
                params=params,
                headers=headers,
                timeout=15,
            )

            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            return parse_rates(
                soup,
                source_currency,
                amount,
            )

        except requests.RequestException as error:
            last_error = error

            if attempt < retries - 1:
                time.sleep(2 ** attempt)

    raise RuntimeError(
        f"Could not retrieve X-Rates data: {last_error}"
    )


def parse_rates(soup, source_currency, amount):
    """Extract currencies and rates from the X-Rates HTML."""

    rates = {}

    tables = soup.find_all("table")

    if not tables:
        raise RuntimeError(
            "No exchange-rate tables found. "
            "X-Rates may have changed its page structure."
        )

    for table in tables:
        for row in table.find_all("tr"):
            cells = row.find_all("td")

            if len(cells) < 2:
                continue

            currency_name = cells[0].get_text(
                " ",
                strip=True
            )

            rate_text = cells[1].get_text(
                " ",
                strip=True
            )

            try:
                rate = float(
                    rate_text.replace(",", "")
                )
            except ValueError:
                continue

            rates[currency_name] = {
                "rate": rate,
                "amount": amount * rate,
            }

    if not rates:
        raise RuntimeError(
            "No exchange rates were extracted."
        )

    return {
        "source_currency": source_currency,
        "amount": amount,
        "retrieved_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "rates": rates,
    }


def filter_rates(data, search=None, minimum=None):
    """Filter currencies by name and/or minimum rate."""

    filtered = {}

    for currency, values in data["rates"].items():

        if search:
            if search.lower() not in currency.lower():
                continue

        if minimum is not None:
            if values["rate"] < minimum:
                continue

        filtered[currency] = values

    data["rates"] = filtered

    return data


def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )


def save_csv(data, filename):
    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Source Currency",
            "Amount",
            "Target Currency",
            "Rate",
            "Converted Amount",
        ])

        for currency, values in data["rates"].items():
            writer.writerow([
                data["source_currency"],
                data["amount"],
                currency,
                values["rate"],
                values["amount"],
            ])


def print_rates(data):
    print()
    print(
        f'{data["amount"]} {data["source_currency"]}'
    )
    print("-" * 60)

    for currency, values in data["rates"].items():
        print(
            f'{currency:<35} '
            f'{values["amount"]:>12,.4f}'
        )

    print("-" * 60)
    print(f'Currencies: {len(data["rates"])}')
    print(f'Retrieved: {data["retrieved_at"]}')


def main():
    parser = argparse.ArgumentParser(
        description="X-Rates currency scraper"
    )

    parser.add_argument(
        "currency",
        help="Source currency, e.g. USD",
    )

    parser.add_argument(
        "-a",
        "--amount",
        type=float,
        default=1,
        help="Amount to convert",
    )

    parser.add_argument(
        "-f",
        "--filter",
        help="Filter currencies by name",
    )

    parser.add_argument(
        "--min-rate",
        type=float,
        help="Only show rates >= this value",
    )

    parser.add_argument(
        "--json",
        help="Save results to JSON",
    )

    parser.add_argument(
        "--csv",
        help="Save results to CSV",
    )

    args = parser.parse_args()

    if args.amount <= 0:
        parser.error("Amount must be greater than 0.")

    data = scrape_xrates(
        args.currency,
        args.amount,
    )

    data = filter_rates(
        data,
        search=args.filter,
        minimum=args.min_rate,
    )

    print_rates(data)

    if args.json:
        save_json(data, args.json)
        print(f"\nSaved JSON: {args.json}")

    if args.csv:
        save_csv(data, args.csv)
        print(f"Saved CSV: {args.csv}")


if __name__ == "__main__":
    main()