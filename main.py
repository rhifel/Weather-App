import sys 
import requests
import os
from dotenv import load_dotenv
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, 
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(r"icons\\clouds.png"))
        
        self.city_label = QLabel("Enter City Name: ", self)        
        
        self.city_input = QLineEdit(self)
        
        self.get_weather_button = QPushButton("Get Weather", self)
        
        self.temperature_label = QLabel(self)
        
        self.emoji_label = QLabel(self)

        self.description_label = QLabel(self)
        
        icons_path = r"E:\Programming\Weather App\icons"
        self.weather_icons = {
                                "thunderstorm": os.path.join(icons_path, "thunderstorm.png"),
                                "drizzle": os.path.join(icons_path, "drizzle.png"),
                                "rain": os.path.join(icons_path, "rain.png"),
                                "snow": os.path.join(icons_path, "snow.png"),
                                "fog": os.path.join(icons_path, "fog.png"),
                                "volcano": os.path.join(icons_path, "volcano.png"),
                                "wind": os.path.join(icons_path, "wind.png"),
                                "tornado": os.path.join(icons_path, "tornado.png"),
                                "clear": os.path.join(icons_path, "clear.png"),
                                "clouds": os.path.join(icons_path, "clouds.png"),
                            }

        self.initUI()
        
        
    def initUI(self):
        self.setWindowTitle("Weather App")
        
        vbox = QVBoxLayout()
        ui_elements = [self.city_label, self.city_input, self.get_weather_button,
                   self.temperature_label, self.emoji_label, self.description_label] # store in a list 
        
        for element in ui_elements: # use for loop for better structure
            vbox.addWidget(element) 
            
        # old code
        # vbox.addWidget(self.city_label)
        # vbox.addWidget(self.city_input)
        # vbox.addWidget(self.get_weather_button)
        # vbox.addWidget(self.temperature_label)
        # vbox.addWidget(self.emoji_label)
        # vbox.addWidget(self.description_label)
        
        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("weather")
        self.temperature_label.setObjectName("temp")
        self.emoji_label.setObjectName("emoji")
        self.description_label.setObjectName("description")
        
        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: Calibri;
            }
            
            QLabel#city_label{
                font-size: 40px;
                font-style: Italic;
            }
            
            QLineEdit#city_input{
                font-size: 40px;
            }
            
            QPushButton#weather{
                font-size: 30px;
                font-weight: bold;
            }
            
            QLabel#temp{
                font-size: 75px;
            }
            
            QLabel#emoji{
                font-size: 100px;
                font-family: "Segoe UI Emoji";
            }
            
            QLabel#description{
                font-size: 50px;
            }
    """)
        
        self.get_weather_button.clicked.connect(self.get_weather)
            
    def get_weather(self):
        load_dotenv()
        
        api_key = os.getenv("API_key")
        base_url = os.getenv("BASE_URL")
        
        city = self.city_input.text()
        
        params = {
            "q": city,
            "appid": api_key,
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data["cod"] == 200:
                self.display_weather(data)
                
        except requests.exceptions.HTTPError as http_err:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess Denied")
                case 404:
                    self.display_error("Not Found:\nCity not Found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gatewayt:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nService is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error ocurred:\n{http_err}")
                    
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects:\nCheck the URL")
        
        except requests.exceptions.RequestException as req_err:
            self.display_error(f"Request Error:\n{req_err}")
        
        
    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
    
    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temp_K = data["main"]["temp"]
        temp_C = temp_K - 273.15
        
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]
        
        self.temperature_label.setText(f"{temp_C:.0f}°C")
        
        #self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.set_weather_icon(self.get_weather_icon_path(weather_id))
        
        self.description_label.setText(weather_description)
    
    def set_weather_icon(self, icon_path, size=150):
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            scaled = pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.emoji_label.setPixmap(scaled)
        else:
            self.emoji_label.clear()
            
    def get_weather_icon_path(self, weather_id):
        if 200 <= weather_id <= 232:
            return self.weather_icons["thunderstorm"]
        
        elif 300 <= weather_id <= 321:
            return self.weather_icons["drizzle"]
        
        elif 500 <= weather_id <= 531:
            return self.weather_icons["rain"]
        
        elif 600 <= weather_id <= 622:
            return self.weather_icons["snow"]
        
        elif 701 <= weather_id <= 741:
            return self.weather_icons["fog"]
        
        elif weather_id == 762:
            return self.weather_icons["volcano"]
        
        elif weather_id == 771:
            return self.weather_icons["wind"]
        
        elif weather_id == 781:
            return self.weather_icons["tornado"]
        
        elif weather_id == 800:
            return self.weather_icons["clear"]
        
        elif 801 <= weather_id <= 804:
            return self.weather_icons["clouds"]
        
        else:
            return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())