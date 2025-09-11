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
        df.to_csv(output_file, index=False)

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
