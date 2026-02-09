from flask import Flask, render_template, request
import joblib
import numpy as np
import requests

app = Flask(__name__)

# Load trained model
model = joblib.load("model/wind_model.pkl")

API_KEY = "f572753249bd896a876c99df49bbd00c"   # put your OpenWeather API key

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    city = request.form['city']
    theoretical_power = float(request.form['theoretical_power'])

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Error handling
    if response.status_code != 200 or 'wind' not in data:
        return render_template(
            'index.html',
            error="Invalid city name or weather data not available."
        )

    wind_speed = data['wind']['speed']
    wind_direction = data['wind'].get('deg', 0)

    input_data = np.array([[wind_speed, wind_direction, theoretical_power]])
    prediction = model.predict(input_data)[0]

    return render_template(
        'index.html',
        city=city,
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        prediction=prediction
    )

if __name__ == "__main__":
    app.run(debug=False)