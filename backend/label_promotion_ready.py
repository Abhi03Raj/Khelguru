import pandas as pd
import json

# Load original player data
csv_file = "player_data_1000.csv"
df = pd.read_csv(csv_file)
df.columns = df.columns.str.strip()  # Clean column names

# Load standard stats from JSON
with open("standard_stats.json") as f:
    standards = json.load(f)

# Function to check if stats meet/exceed tier standard
def check_promotion_ready(row):
    tier = row["Tier"]
    if tier not in standards:
        return 0
    std = standards[tier]
    return int(
        row["K/D_Ratio"] >= std["K/D_Ratio"] and
        row["Avg_Damage"] >= std["Avg_Damage"] and
        row["Survival_Time"] >= std["Survival_Time"] and
        row["Win_Rate (%)"] >= std["Win_Rate (%)"] and
        row["Headshot_Rate (%)"] >= std["Headshot_Rate (%)"]
    )

# Add new column without modifying other data
df["Promotion_Ready"] = df.apply(check_promotion_ready, axis=1)

# Overwrite the same CSV file with new column added
df.to_csv(csv_file, index=False)
print("✅ player_data_1000.csv updated with Promotion_Ready column")
