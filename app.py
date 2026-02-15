from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "f572753249bd896a876c99df49bbd00c"

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    prediction = None
    city = None

    if request.method == "POST":

        # WEATHER BUTTON
        if "check_weather" in request.form:
            city = request.form["city"]

            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                weather = {
                    "temp": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind": data["wind"]["speed"]
                }
            else:
                weather = "error"

        # PREDICT BUTTON
        if "predict_energy" in request.form:
            power = float(request.form["power"])
            wind_speed = float(request.form["wind_speed"])

            # Simple formula (demo purpose)
            prediction = round(power * (wind_speed ** 3) * 0.0001, 2)

    return render_template(
        "index.html",
        city=city,
        weather=weather,
        prediction=prediction
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
