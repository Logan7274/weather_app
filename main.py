import sys
import requests
from PyQt5.QtWidgets import (QApplication , QWidget , QLabel , QLineEdit
                            , QPushButton , QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: " , self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather" , self)
        self.temperature = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel( self)
        self.humid_emoji = QLabel(self)
        self.wind_label = QLabel(self)
        self.initui()

    def initui(self):
        self.setWindowTitle("Weather APP")

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.humid_emoji)
        vbox.addWidget(self.wind_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.humid_emoji.setAlignment(Qt.AlignCenter)
        self.wind_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.temperature.setObjectName("temperature")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.get_weather_button.setObjectName("get_weather_button")

        self.setStyleSheet("""
        
            QLabel , QPushButton , QLineEdit{
                font-family : calibri;
            }
            QLabel#city_label{
                font-size : 40px;
                font-style : italic;
            }
            QLineEdit#city_input{
                font-size : 40px;
            }
            QPushButton#get_weather_button{
                font-size : 30px;
                font-weight : bold;
            }
            QLabel#temperature{
                font-size : 75px;
            }
            QLabel#emoji_label{
                font-size : 100px;
                font-family : Segoe UI emoji;
            }
            QLabel#description_label{
                font-size : 50px;
            }
            
        
        """)

        self.get_weather_button.clicked.connect(self.get_weather)


    def get_weather(self):
        api = "367aeca0c13d35b46ced0db2de60134c"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}"


        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("bad request,\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized,\nInvalid API key")
                case 403:
                    self.display_error("Forbidden,\nAccess is denied")
                case 404:
                    self.display_error("Not found,\nCity not found")
                case 500:
                    self.display_error("Internal Sever Error,\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway,\nInvalid response from the sever")
                case 503:
                    self.display_error("Service Unavailable,\nSever is down")
                case 504:
                    self.display_error("Gateway timeout,\nNo response from the sever")
                case _:
                    self.display_error(f"HTTP error occured,\n {http_error}")


        except requests.exceptions.ConnectionError:
            self.display_error("Connection error,\nPlease check your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("timeout error,\nthe request time out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects,\ncheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error,\n{req_error}")



    def display_error(self , message):
        self.temperature.setStyleSheet("font-size: 30px;"
                                       "color: red;")
        self.temperature.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self , data):
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        humid = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        self.temperature.setStyleSheet("color: black;"
                                       "font-size : 75px;")
        self.temperature.setText(f"🌡️ {temperature_c:.0f}°C")
        self.humid_emoji.setStyleSheet("font-size : 60px;")
        self.wind_label.setStyleSheet("font-size : 60px;")
        weather_description = data["weather"][0]["description"]
        self.description_label.setText(weather_description)
        weather_id = data["weather"][0]["id"]
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.humid_emoji.setText(f"💦 {humid} %")
        self.wind_label.setText(f"🍃 {wind} m/s")

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "☁️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 700 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "🍃"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Weather_app = WeatherApp()
    Weather_app.show()
    sys.exit(app.exec_())
