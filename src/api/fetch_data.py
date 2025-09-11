import requests
import pandas as pd
import os
from datetime import datetime

timestamp = datetime.now().strftime("%H%M%S")



def get_balance_sheet(ticker, api_key):
    balance_sheet_url = "https://financialmodelingprep.com/stable/balance-sheet-statement?symbol="
    output_dir = os.getenv("OUTPUT_PATH")
    timestamp = datetime.now().strftime("%H%M%S")
    output_file = os.path.join(output_dir, f"{timestamp}{ticker}_balance_sheet.csv")

    url = f"{balance_sheet_url}{ticker}&apikey={api_key}"
    #print(f"\n API URL: {url}")  # Show the full URL in the terminal
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data:
            #print("\n JSON Response Received")
            df = pd.DataFrame(data)

            #print("\n DataFrame Preview: ")
            #print(df.head())

            # Save DataFrame to CSV with headers
            #df.to_csv(output_file, index=False, header=True)
            #print(f"\n CSV file saved to: {output_file}")

            return df
        else:
            print("No data found for that ticker.")
            return pd.DataFrame()
    else:
        print(f"Error: {response.status_code}")
        return pd.DataFrame()

def get_income_statement(ticker, api_key):
    income_statement_url = "https://financialmodelingprep.com/stable/income-statement?symbol="
    output_dir = os.getenv("OUTPUT_PATH")
    output_file = os.path.join(output_dir, f"{timestamp}{ticker}_income_statement.csv")
    url = f"{income_statement_url}{ticker}&apikey={api_key}"
    #print("\n JSON Income Statement Response Received")
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data:
            #print("\n JSON Response Received")
            df = pd.DataFrame(data)

            #print("\n DataFrame Preview: ")
            #print(df.head())

            # Save DataFrame to CSV with headers
            #df.to_csv(output_file, index=False, header=True)
            #print(f"\n CSV file saved to: {output_file}")

            return df
        else:
            print("No data found for that ticker.")
            return pd.DataFrame()
    else:
        print(f"Error: {response.status_code}")
        return pd.DataFrame()

def get_cash_flow_statement(ticker, api_key):
    cash_flow_url = "https://financialmodelingprep.com/stable/cash-flow-statement?symbol="
    url = f"{cash_flow_url}{ticker}&apikey={api_key}"
    #print(f"\n API URL: {url}")  # Show the full URL in the terminal
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            #print("\n JSON Response Received")
            df = pd.DataFrame(data)
            #print("\n DataFrame Preview: ")
            #print(df.head())
            return df
        else:
            print("No data found for that ticker.")
            return pd.DataFrame()
    else:
        print(f"Error: {response.status_code}")
        return pd.DataFrame()
          
def get_market_cap(ticker, api_key):
    market_cap_url = "https://financialmodelingprep.com/stable/market-capitalization?symbol="
    url = f"{market_cap_url}{ticker}&apikey={api_key}"
    #print(f"\n API URL: {url}")  # Show the full URL in the terminal
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            #print("\n JSON Response Received")
            df = pd.DataFrame(data)
            #print("\n DataFrame Preview: ")
            #print(df.head())
            return df
        else:
            print("No data found for that ticker.")
            return pd.DataFrame()
    else:
        print(f"Error: {response.status_code}")
        return pd.DataFrame()