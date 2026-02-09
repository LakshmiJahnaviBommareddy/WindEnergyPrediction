import os
import joblib
import pandas as pd
import numpy as np
import requests
from flask import Flask, render_template, request
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)

# =========================
# PATHS & API KEY
# =========================
MODEL_PATH = "model/wind_model.pkl"
DATA_PATH = "dataset/wind_turbine.csv"
API_KEY = os.environ.get("f572753249bd896a876c99df49bbd00c")  # API key from Render env

# =========================
# CREATE MODEL FOLDER
# =========================
os.makedirs("model", exist_ok=True)

# =========================
# LOAD OR TRAIN MODEL
# =========================
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    df = pd.read_csv(DATA_PATH)

    X = df[['Wind Speed (m/s)', 'Wind Direction (°)', 'Theoretical_Power_Curve (KWh)']]
    y = df['LV ActivePower (kW)']

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)

# =========================
# ROUTES
# =========================
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    city = request.form['city']

    # -------------------------
    # OPENWEATHER API CALL
    # -------------------------
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return render_template(
            'index.html',
            prediction_text="Invalid city name or API error"
        )

    wind_speed = data['wind']['speed']           # m/s
    wind_direction = data['wind']['deg']         # degrees

    # -------------------------
    # THEORETICAL POWER (APPROX)
    # -------------------------
    theoretical_power = (wind_speed ** 3) * 0.5

    # -------------------------
    # MODEL PREDICTION
    # -------------------------
    input_data = np.array([[wind_speed, wind_direction, theoretical_power]])
    prediction = model.predict(input_data)[0]

    return render_template(
        'index.html',
        city=city,
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        prediction=round(prediction, 2)
    )


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)