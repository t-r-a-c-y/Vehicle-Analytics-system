import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np

df = pd.read_csv("../../dummy-data/vehicles_ml_dataset.csv")

SEGMENT_FEATURES = ["estimated_income", "selling_price", "kilometers_driven"]  # Added feature for better separation

X = df[SEGMENT_FEATURES]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=4, random_state=42, n_init="auto")  # Increased to 4 for higher silhouette
df["cluster_id"] = kmeans.fit_predict(X_scaled)

centers = kmeans.cluster_centers_
sorted_clusters = centers[:, 0].argsort()  # Sort by scaled income

cluster_mapping = {
    sorted_clusters[0]: "Economy",
    sorted_clusters[1]: "Standard",
    sorted_clusters[2]: "Premium",
    sorted_clusters[3]: "Luxury",
}

df["client_class"] = df["cluster_id"].map(cluster_mapping)

joblib.dump(kmeans, "clustering_model.pkl")

silhouette_avg = round(silhouette_score(X_scaled, df["cluster_id"]), 2)  # Should be >0.9

cluster_summary = df.groupby("client_class")[SEGMENT_FEATURES].mean()
cluster_counts = df["client_class"].value_counts().reset_index()
cluster_counts.columns = ["client_class", "count"]
cluster_summary = cluster_summary.merge(cluster_counts, on="client_class")

comparison_df = df[["client_name", "estimated_income", "selling_price", "client_class"]]

# Exercise b: Coefficient of Variation (CV)
cv_df = pd.DataFrame()
for feature in SEGMENT_FEATURES:
    cv = (df.groupby('client_class')[feature].std() / df.groupby('client_class')[feature].mean()) * 100
    cv_df[f'CV_{feature} (%)'] = cv.round(2)

cv_df['client_class'] = cv.index

def evaluate_clustering_model():
    return {
        "silhouette": silhouette_avg,
        "summary": cluster_summary.to_html(classes="table table-bordered table-striped table-sm", float_format="%.2f", justify="center", index=False),
        "comparison": comparison_df.head(10).to_html(classes="table table-bordered table-striped table-sm", float_format="%.2f", justify="center", index=False),
        "cv_table": cv_df.to_html(classes="table table-bordered table-striped table-sm", float_format="%.2f", justify="center", index=False),  # Display CV
    }