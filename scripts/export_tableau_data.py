import os
import pandas as pd

def export_tableau_data():
    os.makedirs("data", exist_ok=True)
    df = pd.read_parquet("data/processed_parquet")
    output_csv = "data/tableau_ev_battery_health.csv"
    df.to_csv(output_csv, index=False)
    print(f"Tableau-ready dataset successfully exported to: {output_csv} ({len(df)} rows)")

if __name__ == "__main__":
    export_tableau_data()
