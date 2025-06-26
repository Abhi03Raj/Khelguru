import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load player data
file_path = "player_data_1000.csv"
df = pd.read_csv(file_path)

# Group by tier
tiers = df["Tier"].unique()
standard_stats = {}

# Features to consider for standard performance
features = [
    "K/D_Ratio",
    "Avg_Damage",
    "Survival_Time",
    "Win_Rate (%)",
    "Headshot_Rate (%)"
]

# Generate stats per tier
for tier in tiers:
    tier_df = df[df["Tier"] == tier]
    X = tier_df[features].dropna()

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Clustering to identify top performance group
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    centroids = scaler.inverse_transform(kmeans.cluster_centers_)

    # Select cluster with highest average K/D ratio
    cluster_kd = centroids[:, features.index("K/D_Ratio")]
    top_cluster_idx = np.argmax(cluster_kd)
    top_cluster_stats = dict(zip(features, centroids[top_cluster_idx]))

    # Optionally: Fallback to 75th percentile if needed
    # percentile_stats = X.quantile(0.75).to_dict()

    standard_stats[tier] = top_cluster_stats

# Save to JSON
with open("standard_stats.json", "w") as f:
    json.dump(standard_stats, f, indent=2)

print("✅ Advanced standard stats saved to standard_stats.json")
