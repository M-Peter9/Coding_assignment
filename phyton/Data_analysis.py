# -----------------------------------------------
# Python Data Analysis Script
# Task: Income comparison + Solow model
# Author: Péter Márton
# -----------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Set up folder structure
base_dir = "C:/Users/User/OneDrive/Dokumentumok/suli/Egyetem/CEU/coding/Assignment"
raw_dir = os.path.join(base_dir, "data/raw")
cleaned_dir = os.path.join(base_dir, "data/cleaned")
graphs_dir = os.path.join(base_dir, "graphs")

os.makedirs(cleaned_dir, exist_ok=True)
os.makedirs(graphs_dir, exist_ok=True)

# 2. Load Excel data
file_path = os.path.join(raw_dir, "pwt110.xlsx")
df = pd.read_excel(file_path, sheet_name="Data")

# --- Data quality fixes ---
# Convert rgdpo and rgdpe to numeric (if needed)
df["rgdpo"] = pd.to_numeric(df["rgdpo"], errors="coerce")
df["rgdpe"] = pd.to_numeric(df["rgdpe"], errors="coerce")

# Drop rows with missing values in key columns
df_cleaned = df.dropna(subset=["country", "year", "rgdpo", "rgdpe", "pop", "emp", "cn"])

# Save cleaned version
df_cleaned.to_csv(os.path.join(cleaned_dir, "pwt_cleaned.csv"), index=False)


file_path = os.path.join(cleaned_dir, "pwt_cleaned.csv")
df = pd.read_csv(file_path)

# --- Analysis ---
# 3. Select relevant columns
cols = ["country", "year", "rgdpo", "rgdpe", "cn", "pop", "emp"]
df = df[cols]

# 4. Filter for year 2023
df_2023 = df[df["year"] == 2023].copy()

# 5. Create transformed variables
df_2023["y_per_person"] = df_2023["rgdpo"]  / df_2023["pop"]
df_2023["y_per_worker"] = df_2023["rgdpo"]  / df_2023["emp"]

# 6. Compute income relative to US
us_income = df_2023.loc[df_2023["country"] == "United States", "y_per_person"].values[0]
df_2023["rel_income_US"] = df_2023["y_per_person"] / us_income

# 7. Select countries of interest
countries = ["China", "India", "France", "Vietnam", "Nigeria", "Brazil", "Hungary"]
comparison = df_2023[df_2023["country"].isin(countries)][
    ["country", "y_per_person", "y_per_worker", "rel_income_US"]
]
comparison = comparison.sort_values(by="rel_income_US", ascending=False)

# 8. Plot income relative to US
plt.figure(figsize=(8, 5))
sns.barplot(data=comparison, x="rel_income_US", y="country", color="steelblue")
plt.title("Per-capita Income Relative to the US (2023)")
plt.xlabel("Income relative to US")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig(os.path.join(graphs_dir, "income_relative_to_US.png"), dpi=300)
plt.close()

# 9. Solow model setup
alpha = 1/3
df_2023["k_per_worker"] = df_2023["cn"]  / df_2023["emp"]
df_2023["ln_y"] = np.log(df_2023["y_per_worker"])
df_2023["ln_k"] = np.log(df_2023["k_per_worker"])

solow_data = df_2023.dropna(subset=["ln_y", "ln_k"]).copy()

# 10. Equal technology assumption
lnZ_Solow = (solow_data["ln_y"].mean() - alpha * solow_data["ln_k"].mean()) / (1 - alpha)
Z_Solow = np.exp(lnZ_Solow)

solow_data["ln_y_hat_Solow"] = alpha * solow_data["ln_k"] + (1 - alpha) * lnZ_Solow

# Plot predicted vs actual ln y
plt.figure(figsize=(7, 5))
sns.scatterplot(data=solow_data, x="ln_y", y="ln_y_hat_Solow", color="steelblue")
plt.plot([solow_data["ln_y"].min(), solow_data["ln_y"].max()],
         [solow_data["ln_y"].min(), solow_data["ln_y"].max()],
         linestyle="--", color="red")
plt.title("Solow Model Prediction (Equal Technology)")
plt.xlabel("Actual ln output per worker")
plt.ylabel("Predicted ln output per worker")
plt.tight_layout()
plt.savefig(os.path.join(graphs_dir, "solow_equaltech_lnY_vs_lnYhat.png"), dpi=300)
plt.close()

# 11. Implied productivity lnZ_i
solow_data["lnZ_implied"] = (solow_data["ln_y"] - alpha * solow_data["ln_k"]) / (1 - alpha)

# Plot lnZ_implied vs ln_y
plt.figure(figsize=(7, 5))
sns.scatterplot(data=solow_data, x="ln_y", y="lnZ_implied", color="steelblue")
sns.regplot(data=solow_data, x="ln_y", y="lnZ_implied", scatter=False, color="darkorange")
plt.title("Implied ln Z_i vs ln y")
plt.xlabel("ln output per worker")
plt.ylabel("Implied ln Z_i")
plt.tight_layout()
plt.savefig(os.path.join(graphs_dir, "implied_lnZ_vs_lnY.png"), dpi=300)
plt.close()

# 12. Steady-state inversion
ln_psi = solow_data["ln_k"].mean() - lnZ_Solow
psi = np.exp(ln_psi)

solow_data["lnZ_tilde"] = solow_data["ln_k"] - ln_psi
solow_data["ln_y_hat_full"] = alpha * solow_data["ln_k"] + (1 - alpha) * solow_data["lnZ_tilde"]

# Plot full model prediction
plt.figure(figsize=(7, 5))
sns.scatterplot(data=solow_data, x="ln_y", y="ln_y_hat_full", color="forestgreen")
sns.regplot(data=solow_data, x="ln_y", y="ln_y_hat_full", scatter=False, color="darkblue")
plt.plot([solow_data["ln_y"].min(), solow_data["ln_y"].max()],
         [solow_data["ln_y"].min(), solow_data["ln_y"].max()],
         linestyle="--", color="red")
plt.title("Full Model Prediction (Steady-State Inversion)")
plt.xlabel("Actual ln output per worker")
plt.ylabel("Predicted ln output per worker")
plt.tight_layout()
plt.savefig(os.path.join(graphs_dir, "solow_fullmodel_lnYhat_vs_lnY.png"), dpi=300)
plt.close()

# 13. Save computed and cleaned data
solow_data.to_csv(os.path.join(cleaned_dir, "solow_computed_columns.csv"), index=False)

# 14. Additional plots for comparison countries

metrics = {
    "y_per_person": "Income per Person (USD)",
    "y_per_worker": "Income per Worker (USD)"
}

for metric, label in metrics.items():
    plt.figure(figsize=(8, 5))
    sns.barplot(data=comparison, x=metric, y="country", color="steelblue")
    plt.title(f"{label} by Country (2023)")
    plt.xlabel(label)
    plt.ylabel("Country")
    plt.tight_layout()
    plt.savefig(os.path.join(graphs_dir, f"{metric}_barplot.png"), dpi=300)
    plt.close()


# 15. Summary statistics
summary = df_2023[["y_per_person", "y_per_worker", "rel_income_US"]].describe()
print(summary)

# Save to CSV
summary.to_csv(os.path.join(cleaned_dir, "summary_statistics.csv"))