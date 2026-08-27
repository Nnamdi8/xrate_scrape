import sys
import re
import requests
from bs4 import BeautifulSoup as bs
from dateutil.parser import parse


def get_digits(text):
    """Extract a numeric value from text."""

    # Remove commas and keep digits, decimal point, and minus sign
    cleaned = re.sub(r"[^\d.-]", "", text)

    if not cleaned:
        raise ValueError(f"Could not find a number in: {text}")

    return float(cleaned)


def convert_currency_xe(src, dst, amount):
    """Get a currency conversion from XE."""

    src = src.upper()
    dst = dst.upper()

    url = (
        "https://www.xe.com/currencyconverter/convert/"
        f"?Amount={amount}&From={src}&To={dst}"
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/139.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    response.raise_for_status()

    soup = bs(response.text, "html.parser")

    # Look for paragraphs containing the conversion result
    paragraphs = soup.find_all("p")

    exchange_rate = None

    for paragraph in paragraphs:
        text = paragraph.get_text(" ", strip=True)

        # Look for text containing the source and destination currencies
        if src in text and dst in text:
            try:
                exchange_rate = get_digits(text)
                break
            except ValueError:
                continue

    if exchange_rate is None:
        # Try looking for a conversion-rate pattern
        page_text = soup.get_text(" ", strip=True)

        pattern = rf"1\s*{re.escape(src)}\s*=\s*([\d,.]+)\s*{re.escape(dst)}"

        match = re.search(pattern, page_text, re.IGNORECASE)

        if match:
            exchange_rate = get_digits(match.group(1))

    if exchange_rate is None:
        raise RuntimeError(
            "Could not find the exchange rate on the XE page. "
            "XE may have changed its HTML structure or requires "
            "JavaScript to render the rate."
        )

    # Find "Last updated" information
    last_updated_datetime = None

    page_text = soup.get_text(" ", strip=True)

    match = re.search(
        r"Last updated\s*[:\-]?\s*(.+?)(?=\s{2,}|$)",
        page_text,
        re.IGNORECASE
    )

    if match:
        try:
            last_updated_datetime = parse(
                match.group(1).strip(),
                fuzzy=True
            )
        except (ValueError, OverflowError):
            pass

    return last_updated_datetime, exchange_rate


def main():
    if len(sys.argv) != 4:
        print(
            "Usage: python xe_scraper.py "
            "SOURCE DESTINATION AMOUNT"
        )
        print()
        print("Example:")
        print("python xe_scraper.py USD GBP 100")
        sys.exit(1)

    source_currency = sys.argv[1].upper()
    destination_currency = sys.argv[2].upper()

    try:
        amount = float(sys.argv[3])
    except ValueError:
        print("Amount must be a number.")
        sys.exit(1)

    if amount <= 0:
        print("Amount must be greater than zero.")
        sys.exit(1)

    try:
        last_updated_datetime, exchange_rate = convert_currency_xe(
            source_currency,
            destination_currency,
            amount
        )

        print(
            "Last updated datetime:",
            last_updated_datetime
        )

        print(
            f"{amount:,.2f} {source_currency} = "
            f"{exchange_rate:,.2f} {destination_currency}"
        )

    except requests.RequestException as error:
        print(f"Request failed: {error}")
        sys.exit(1)

    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()