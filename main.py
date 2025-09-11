from dotenv import load_dotenv
import os
from src.db.db_setup import initialize_db
from src.api.fetch_data import get_balance_sheet, get_income_statement, get_cash_flow_statement, get_market_cap
from src.analysis.financial_health import calculate_altman_z_score, calculate_free_cash_flow, get_z_score_zone,fcf_to_debt_category

# Load environment variables from .env file
load_dotenv()

# Initialize the database
initialize_db()

if __name__ == "__main__":
    ticker = input("Enter the stock ticker symbol (e.g., AAPL): ").upper()
    api_key = os.getenv("FMP_API_KEY")

    balance_sheet = get_balance_sheet(ticker, api_key)
    income_statement = get_income_statement(ticker, api_key)
    cash_flow_statement = get_cash_flow_statement(ticker, api_key)
   
    
    market_cap = get_market_cap(ticker, api_key)

    z_altman_score = calculate_altman_z_score(balance_sheet, income_statement, market_cap)
    free_cash_flow = calculate_free_cash_flow(cash_flow_statement)
    total_debt = balance_sheet.loc[0, 'totalDebt']

    zone, description = get_z_score_zone(z_altman_score)

    print(f"\nAltman Z-Score for {ticker}: {z_altman_score}")
    print(f"Zone: {zone}")
    print(f"Description: {description}")
    print(f"\nFree Cash Flow for {ticker}: ${free_cash_flow:,.2f}")
    print(f"Total Debt: ${total_debt:,.2f}")
    fcf_debt_analysis = fcf_to_debt_category(free_cash_flow, total_debt)
    print(fcf_debt_analysis)
    print(f"\n")
    print(f"\n")