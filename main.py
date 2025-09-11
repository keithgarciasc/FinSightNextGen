from dotenv import load_dotenv
import os
from src.api.fetch_data import get_balance_sheet, get_income_statement, get_market_cap
from src.analysis.financial_health import calculate_altman_z_score, get_z_score_zone

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    ticker = input("Enter the stock ticker symbol (e.g., AAPL): ").upper()
    api_key = os.getenv("FMP_API_KEY")

    balance_sheet = get_balance_sheet(ticker, api_key)
    income_statement = get_income_statement(ticker, api_key)
    market_cap = get_market_cap(ticker, api_key)
    z_altman_score = calculate_altman_z_score(balance_sheet, income_statement, market_cap)

    zone, description = get_z_score_zone(z_altman_score)
    print(f"\nAltman Z-Score for {ticker}: {z_altman_score}")
    print(f"Zone: {zone}")
    print(f"Description: {description}")