import pandas as pd

# Load the CSV
df = pd.read_csv("data/pernambuco_emissions_by_sectors.csv", encoding="utf-8")

# Reshape from wide to long format
df_long = df.melt(
    id_vars=["Categoria"], var_name="year", value_name="emissions_metric_tons"
)

# Clean column names
df_long.columns = ["sector", "year", "emissions_metric_tons"]

# Save cleaned data
df_long.to_csv("data/pernambuco_co2_clean.csv", index=False)
