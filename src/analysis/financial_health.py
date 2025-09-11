import pandas as pd

Z_SCORE_ZONES = {
    "Safe Zone": {
        "min": 2.99,
        "max": float("inf"),
        "description": "The company is financially healthy with a low risk of bankruptcy."
    },
    "Grey Zone": {
        "min": 1.81,
        "max": 2.99,
        "description": "The company is in a cautionary zone; financial health is uncertain and should be monitored."
    },
    "Distress Zone": {
        "min": float("-inf"),
        "max": 1.81,
        "description": "The company is at high risk of financial distress or bankruptcy."
    }
}

def calculate_altman_z_score(balance_sheet: pd.DataFrame, income_statement: pd.DataFrame, market: pd.DataFrame, output_file: str = "altman_z_score_components.csv") -> float:
    try:
        # Extract required values
        current_assets = balance_sheet.loc[0, 'totalCurrentAssets']
        current_liabilities = balance_sheet.loc[0, 'totalCurrentLiabilities']
        total_assets = balance_sheet.loc[0, 'totalAssets']
        retained_earnings = balance_sheet.loc[0, 'retainedEarnings']
        total_liabilities = balance_sheet.loc[0, 'totalLiabilities']

        ebit = income_statement.loc[0, 'ebit']
        revenue = income_statement.loc[0, 'revenue']

        market_value_equity = market.loc[0, 'marketCap']

        # Altman Z-score components
        A = (current_assets - current_liabilities) / total_assets
        B = retained_earnings / total_assets
        C = ebit / total_assets
        D = market_value_equity / total_liabilities
        E = revenue / total_assets

        # Save extracted values to CSV
        data = {
            "current_assets": [current_assets],
            "current_liabilities": [current_liabilities],
            "total_assets": [total_assets],
            "retained_earnings": [retained_earnings],
            "total_liabilities": [total_liabilities],
            "ebit": [ebit],
            "revenue": [revenue],
            "market_value_equity": [market_value_equity],
        }
        df = pd.DataFrame(data)
        #df.to_csv(output_file, index=False)

        # Altman Z-score formula
        z_score = 1.2 * A + 1.4 * B + 3.3 * C + 0.6 * D + 1.0 * E
        return round(z_score, 2)

    except Exception as e:
        print(f"Error calculating Altman Z-score: {e}")
        return None

def get_z_score_zone(z_score: float):
    for zone, info in Z_SCORE_ZONES.items():
        if info["min"] < z_score <= info["max"]:
            return zone, info["description"]
    return "Unknown", "No description available."

def calculate_free_cash_flow(cash_flow_statement: pd.DataFrame) -> float:
    try:
        # Extract required values
        operating_cash_flow = cash_flow_statement.loc[0, 'operatingCashFlow']
        capital_expenditures = cash_flow_statement.loc[0, 'capitalExpenditure']

        # Free Cash Flow components
        ocf = operating_cash_flow
        capex = capital_expenditures

        # Free cash flow formula
        fcf = ocf - capex
        return round(fcf, 2)
    
    except Exception as e:
        print(f"Error calculating Free Cash Flow: {e}")
        return None

def fcf_to_debt_category(fcf: float, total_debt: float) -> str:
    try:
        ratio = (fcf / total_debt) * 100
        if ratio <= 0:
            return f"FCF-to-Debt Ratio: {ratio:.2f}%\nMeaning: Company has no free cash flow or is negative; can't cover any debt.\nFinancial Health: Very risky"
        elif ratio <= 25:
            return f"FCF-to-Debt Ratio: {ratio:.2f}%\nMeaning: FCF covers only a small portion of debt; likely needs external funding.\nFinancial Health: Weak"
        elif ratio <= 50:
            return f"FCF-to-Debt Ratio: {ratio:.2f}%\nMeaning: FCF covers half or less of debt; manageable but still leveraged.\nFinancial Health: Moderate risk"
        elif ratio <= 75:
            return f"FCF-to-Debt Ratio: {ratio:.2f}%\nMeaning: FCF covers most of debt; company is improving its debt position.\nFinancial Health: Fair"
        elif ratio <= 100:
            return f"FCF-to-Debt Ratio: {ratio:.2f}%\nMeaning: FCF nearly covers all debt; strong ability to pay off obligations.\nFinancial Health: Strong"
        else:
            return f"FCF-to-Debt Ratio: {ratio:.2f}%\nMeaning: FCF exceeds total debt; company could pay off all debt in one year.\nFinancial Health: Excellent"

    except ZeroDivisionError:
        return "Error: Total debt cannot be zero."
    except Exception as e:
        return f"Error: {e}"
