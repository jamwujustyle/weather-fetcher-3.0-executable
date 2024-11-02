import sys
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet(
            """
                    QLabel, QPushButton{
                           font-family: calibri;
                    }
                    QLabel#city_label{
                            font-size: 40px;
                            font-style: italic;
                    }
                    QLineEdit#city_input{
                    font-size: 40px;
                    }
                    QPushButton#get_weather_button{
                    font-size: 30px;
                    font-weight: bold;
                    }
                    QLabel#temperature_label{
                    font-size: 75px;
                    }
                    QLabel#emoji_label{
                    font-size: 100px;
                    font-family: Segoe UI emoji;
                    }
                    QLabel#description_label{
                    font-size: 50px;
                    }
            """
        )

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):

        api_key1 = "4c4f3b303b374761b30efcb990942734"
        api_key2 = "b85ee4be00f24563b96125616242210"
        city = self.city_input.text().capitalize()
        url1 = (
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key1}"
        )
        url2 = f"http://api.weatherapi.com/v1/current.json?key={api_key2}&q={city}"

        try:
            response2 = requests.get(url2)
            response2.raise_for_status()
            data2 = response2.json()

            response = requests.get(url1)
            response.raise_for_status()
            data = response.json()

            if response.status_code == 200:
                self.print_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.print_error("Bad Request:\nPlease check your input")
                case 401:
                    self.print_error("Unathorized:\nInvalid API key")
                case 403:
                    self.print_error("Forbidden:\nAccess is denied")
                case 404:
                    self.print_error("Not found:\nCity not found")
                case 500:
                    self.print_error("Internal server error:\nPlease try again later")
                case 502:
                    self.print_error("Bad Gateway:\nInvalid response from server")
                case 503:
                    self.print_error("Servis unavailable:\nServer is down")
                case 504:
                    self.print_error("Gateway timeou:t\nNo response from the server")
                case _:
                    self.print_error(f"HTTP error occured:\n{http_error}")

        except requests.exceptions.ConnectionError:
            print("Connection error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            print("Timeout error\nThe request times dout")
        except requests.exceptions.TooManyRedirects:
            print("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            print(f"Request Error:\n{req_error}")

    def print_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def print_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_k = data["main"]["temp"]
        temperature_c = round(temperature_k - 273.15, 1)
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]
        self.temperature_label.setText(f"{temperature_c:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    def minimize_temperature(self, data, data2):
        temperature_k = data["main"]["temp"]
        temperature_c = round(temperature_k - 273.15, 1)
        temp2 = data2["current"]["temp_c"]
        print(f"from second api {temp2}")
        average = (temperature_c + temp2) / 2
        print(f"average is {average}")

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⚡"
        elif 300 <= weather_id <= 321:
            return "🌥️"
        elif 500 <= weather_id <= 531:
            return "⛈️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "😶‍🌫️"
        else:
            return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())


# 4c4f3b303b374761b30efcb990942734
# https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}
# 2
# b85ee4be00f24563b96125616242210
# http://api.weatherapi.com/v1
