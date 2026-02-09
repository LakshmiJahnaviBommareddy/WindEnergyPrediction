import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("dataset/wind_turbine.csv")

# -----------------------------
# Data Preprocessing
# -----------------------------
# Convert Date/Time safely
df['Date/Time'] = pd.to_datetime(df['Date/Time'], errors='coerce')

# Drop invalid datetime rows
df.dropna(subset=['Date/Time'], inplace=True)

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# -----------------------------
# Feature Selection
# -----------------------------
X = df[['Wind Speed (m/s)',
        'Wind Direction (°)',
        'Theoretical_Power_Curve (KWh)']]

y = df['LV ActivePower (kW)']

# -----------------------------
# Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# Model Building
# -----------------------------
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

# -----------------------------
# Training
# -----------------------------
model.fit(X_train, y_train)

# -----------------------------
# Testing
# -----------------------------
y_pred = model.predict(X_test)

# -----------------------------
# Evaluation
# -----------------------------
print("Model Evaluation Results:")
print("MAE:", mean_absolute_error(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
print("R2 Score:", r2_score(y_test, y_pred))

# -----------------------------
# Save Model
# -----------------------------
joblib.dump(model, "model/wind_model.pkl")

print("✅ Model trained and saved successfully!")