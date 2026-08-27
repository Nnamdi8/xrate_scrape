================================================================================
EXCHANGE RATE SCRAPERS AND CURRENCY CONVERTERS
================================================================================

Welcome! This project is a Python-based collection of exchange-rate scrapers and 
currency conversion utilities. It is designed to show you several different ways 
to fetch and work with foreign-exchange data, from web scraping and financial 
market data to REST APIs. Whether you are learning how to parse HTML, 
experimenting with financial APIs, or just need a quick currency conversion 
script, this repository has you covered.


--------------------------------------------------------------------------------
SUPPORTED PROVIDERS
--------------------------------------------------------------------------------
We support five main providers:

  - X-Rates & XE: 
    Web scraping to grab exchange-rate tables or specific conversions.
    
  - Yahoo Finance: 
    Market data for recent, real-world currency-pair prices.
    
  - ExchangeRate-API & Fixer: 
    REST APIs used for reliable, programmatic exchange rates and conversions.


--------------------------------------------------------------------------------
PROJECT STRUCTURE
--------------------------------------------------------------------------------
The repository is kept neat and tidy. You will find:

  currency_converter_xrates.py
  currency_converter_xe.py
  currency_converter_yahoofin.py
  currency_converter_erapi.py
  currency_converter_fixerapi.py
  README.txt (this file)


--------------------------------------------------------------------------------
WHAT YOU CAN DO
--------------------------------------------------------------------------------
  - Fetch live or recent exchange-rate information.
  - Convert amounts from one currency to another on the fly.
  - Retrieve rates for a whole basket of currencies at once.
  - View timestamps with every retrieval so you know exactly how fresh the 
    data is.
  - Run the same conversion through different tools to compare results.
  - Learn by seeing both web-scraping and API-based approaches in action.
  - Fire up any converter directly from your terminal.


--------------------------------------------------------------------------------
GETTING STARTED
--------------------------------------------------------------------------------
Before we begin, make sure you have:
  - Python 3.8 or newer
  - An active internet connection
  - API credentials for the providers that require them

Double-check your Python version by running:
  python --version

To install:
  1. Clone the repository and change into the directory.
  2. Create a virtual environment: 
       python -m venv .venv
  3. Activate it:
       Linux/macOS: source .venv/bin/activate
       Windows:     .venv\Scripts\activate
  4. Install the dependencies:
       pip install requests beautifulsoup4 python-dateutil yahoo-fin


--------------------------------------------------------------------------------
HOW TO USE IT
--------------------------------------------------------------------------------
All the converters follow the same simple, intuitive pattern in the command 
line:

  SOURCE_CURRENCY DESTINATION_CURRENCY AMOUNT

For example, running:
  python currency_converter_xrates.py USD NGN 100

This tells the script to convert 100 US Dollars to Nigerian Naira.


--------------------------------------------------------------------------------
DEEP DIVE: THE PROVIDERS
--------------------------------------------------------------------------------

1. X-Rates (Web Scraping)
   This script fetches the X-Rates website exchange-rate table and parses the 
   HTML. The core function, get_exchange_list_xrates(currency, amount=1), 
   returns a tuple of the price datetime and a dictionary of exchange rates. 
   
   Note: Because this relies on HTML scraping, if X-Rates changes their 
   website layout, this script might need a quick tune-up.

2. XE Currency Converter (Web Scraping)
   Similar to X-Rates, this tool targets the XE currency converter page to 
   pull a direct conversion value using the convert_currency_xe(src, dst, 
   amount) function. It builds the URL, fetches the page, uses BeautifulSoup 
   to find the converted value, and includes a helper to cleanly extract the 
   numbers. Like X-Rates, it is susceptible to HTML layout changes.

3. Yahoo Finance (Market Data)
   This uses the yahoo_fin package to grab recent, real-world market data for 
   currency pairs via the convert_currency_yahoofin(src, dst, amount) function. 
   Yahoo Finance uses a specific format for currency pairs, such as USDNGN=X 
   or EURUSD=X. It constructs the symbol, grabs the latest one-minute market 
   data record, and multiplies that price by your requested amount. 
   
   Note: Yahoo Finance provides market or reference data, which is great for 
   estimation but not a guaranteed executable rate from a bank.

4. ExchangeRate-API (REST API)
   A clean, reliable JSON-based REST API approach. It features 
   get_all_exchange_rates_erapi(src) to get all rates for a base currency, and 
   convert_currency_erapi(src, dst, amount) to directly convert an amount.

5. Fixer (REST API)
   Fixer offers two ways to play, depending on your account tier. The free 
   account approach calculates a cross-rate using the formula: 
   Exchange Rate = (1 / Source Rate) * Destination Rate. 
   The paid approach uses a direct conversion endpoint via 
   convert_currency_fixerapi(src, dst, amount).


--------------------------------------------------------------------------------
API KEY MANAGEMENT
--------------------------------------------------------------------------------
If you are using Fixer or any API that requires a key, NEVER hardcode your API 
key in your source code. Instead, use environment variables:

  import os
  API_KEY = os.getenv("FIXER_API_KEY")

You can set this in your terminal:
  - Linux/macOS:       export FIXER_API_KEY="your-api-key"
  - Windows PowerShell: $env:FIXER_API_KEY="your-api-key"

For local development, using a .env file and adding it to your .gitignore is 
the industry standard. 

SECURITY WARNING: If you accidentally commit an API key to a public repository, 
consider it compromised and revoke or rotate it immediately through your 
provider's dashboard.


--------------------------------------------------------------------------------
COMMON CURRENCY CODES
--------------------------------------------------------------------------------
We use standard three-letter ISO 4217 codes. Common examples include:

  USD : US Dollar           CAD : Canadian Dollar
  EUR : Euro                AUD : Australian Dollar
  GBP : British Pound       CHF : Swiss Franc
  NGN : Nigerian Naira      JPY : Japanese Yen


--------------------------------------------------------------------------------
PROVIDER COMPARISON
--------------------------------------------------------------------------------
  - X-Rates: 
    HTML scraping, no API key, multiple rates, indirect conversion. 
    Limitation: HTML structure can change.
    
  - XE: 
    HTML scraping, no API key, single conversion. 
    Limitation: HTML structure can change.
    
  - Yahoo Finance: 
    Market data, no API key, pair-based. 
    Limitation: Reference data only.
    
  - ExchangeRate-API: 
    REST API, no key for basic use, multiple rates, direct conversion. 
    Limitation: Provider rate limits.
    
  - Fixer: 
    REST API, requires API key, multiple rates, direct conversion. 
    Limitation: Feature limits on free plans.


--------------------------------------------------------------------------------
UNDER THE HOOD: SCRAPING VS APIS
--------------------------------------------------------------------------------
Web Scraping:
  [Pros] Great for learning, requires no API keys, accesses publicly 
         displayed data.
  [Cons] Fragile (breaks if the website changes), harder to maintain, might 
         hit anti-bot protections, and you must respect the site's Terms of 
         Service.

API Integration:
  [Pros] Clean JSON, easy to parse, built for automation, includes reliable 
         metadata (like timestamps).
  [Cons] Usually requires an API key, subject to rate limits/quotas, and 
         advanced features might cost money.


--------------------------------------------------------------------------------
ERROR HANDLING AND PRODUCTION READINESS
--------------------------------------------------------------------------------
Right now, these scripts are designed to clearly demonstrate the core logic of 
fetching and converting data. If you want to take this to production, you will 
want to beef up the error handling. Think about guarding against network 
dropouts, invalid currency codes, API rate limits, and unexpected changes in 
scraped HTML. 

Pro tip for production: Always use timeouts and validate responses.

  response = requests.get(url, timeout=10)
  response.raise_for_status()


--------------------------------------------------------------------------------
TESTING AND FUTURE IMPROVEMENTS
--------------------------------------------------------------------------------
To make this project even better, consider:

  1. Creating a unified interface with a single convert_currency() function 
     that lets you swap providers seamlessly.
  2. Moving all settings and keys to environment or config files.
  3. Adding resilient HTTP clients with retry logic and strict timeout 
     validations.
  4. Swapping print statements for Python's built-in logging module.
  5. Adding automated tests with mocked API responses.
  6. Building a provider fallback system (if Provider A fails, try Provider B).


--------------------------------------------------------------------------------
EXAMPLE APPLICATION FLOW
--------------------------------------------------------------------------------
  1. User Request (e.g., USD to NGN, Amount: 100)
  2. Currency Converter Script receives the request.
  3. Selected Provider (Scraper OR API) is queried.
  4. Script fetches the Exchange Rate and Timestamp.
  5. Script calculates: Rate * Amount.
  6. Script returns: "100 USD = [X] NGN (Updated at [Time])"


--------------------------------------------------------------------------------
A QUICK WORD ON FINANCIAL DATA
--------------------------------------------------------------------------------
Exchange rates are highly dynamic. The rate returned by these scripts is for 
informational and educational purposes. It may differ from your bank's exchange 
rate, credit card network rates, or money-transfer service rates. Always check 
the timestamp on the data, and for real financial applications, carefully 
evaluate the provider's terms, update frequency, and any hidden transaction 
fees.


--------------------------------------------------------------------------------
CONTRIBUTING
--------------------------------------------------------------------------------
Contributions are absolutely welcome! If you want to add a new provider or 
improve an existing one, please:

  - Create a dedicated, cleanly named Python module.
  - Keep the provider logic isolated and modular.
  - Match the existing conversion interface where possible.
  - Add thoughtful error handling and tests.
  - Update this README to document your changes.
  - NEVER commit API keys or secrets.


--------------------------------------------------------------------------------
LICENSE
--------------------------------------------------------------------------------
No license has currently been specified for this project. If you plan to use 
or distribute this repository publicly, please add an appropriate LICENSE file 
(like MIT or Apache 2.0) and update this section.


--------------------------------------------------------------------------------
SUMMARY
--------------------------------------------------------------------------------
This project is a hands-on exploration of retrieving and converting foreign-
exchange data using a mix of modern techniques, including HTML scraping, market 
data fetching, and REST APIs. It is a perfect sandbox for learning about Python 
HTTP requests, HTML parsing, REST API integration, financial data handling, and 
building resilient provider abstractions. 

Happy coding!
================================================================================
