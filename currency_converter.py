import requests


def get_exchange_rate(from_currency, to_currency):
    url = f"https://open.er-api.com/v6/latest/{from_currency}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    if data["result"] != "success":
        raise Exception("Could not get exchange rates.")

    rates = data["rates"]

    if to_currency not in rates:
        raise ValueError(f"Currency '{to_currency}' was not found.")

    return rates[to_currency]


def convert_currency(amount, from_currency, to_currency):
    rate = get_exchange_rate(from_currency, to_currency)
    converted_amount = amount * rate

    return converted_amount, rate


def main():
    print("=== Currency Converter ===")

    from_currency = input("Convert from (e.g. USD): ").upper()
    to_currency = input("Convert to (e.g. NGN): ").upper()

    try:
        amount = float(input("Enter amount: "))

        if amount <= 0:
            print("Amount must be greater than 0.")
            return

        converted_amount, rate = convert_currency(
            amount,
            from_currency,
            to_currency
        )

        print()
        print(f"{amount:.2f} {from_currency} = "
              f"{converted_amount:.2f} {to_currency}")

        print(f"Exchange rate: 1 {from_currency} = "
              f"{rate:.4f} {to_currency}")

    except ValueError as error:
        print(f"Error: {error}")

    except requests.RequestException:
        print("Error: Could not connect to the exchange-rate service.")

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()