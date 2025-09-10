from dotenv import load_dotenv
import os
from src.api.fetch_data import get_balance_sheet

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    ticker = input("Enter the stock ticker symbol (e.g., AAPL): ").upper()
    api_key = os.getenv("FMP_API_KEY")
    balance_sheet = get_balance_sheet(ticker, api_key)
