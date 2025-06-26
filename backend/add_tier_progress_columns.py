import pandas as pd
import random
from datetime import datetime

# Load the CSV
file_path = 'player_data_1000.csv'
df = pd.read_csv(file_path)

# Always add or overwrite values
now = datetime.now()
current_season = f"S{now.year}_{(now.month - 1) // 2 + 1}"
df['Season'] = current_season
df['Tier_Stage'] = df['Tier'].apply(lambda tier: random.randint(1, 5))
df['Tier_Points'] = df['Tier'].apply(lambda tier: random.randint(0, 99))

# Save updated file
df.to_csv(file_path, index=False)

print("✅ Columns added or updated successfully in player_data_1000.csv")
