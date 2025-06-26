import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load labeled data
df = pd.read_csv("player_data_1000.csv")
df.columns = df.columns.str.strip()

# Encode tier to numeric values
tier_map = {
    "Bronze": 0, "Silver": 1, "Gold": 2,
    "Platinum": 3, "Diamond": 4, "Master": 5, "Grandmaster": 6
}
df["Tier_Num"] = df["Tier"].map(tier_map)

# Features and target
X = df[["K/D_Ratio", "Avg_Damage", "Survival_Time", "Win_Rate (%)", "Headshot_Rate (%)", "Tier_Num"]]
y = df["Promotion_Ready"]

# Train-test split (optional, good practice)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, "promotion_predictor.pkl")
print("✅ Trained and saved as promotion_predictor.pkl")
