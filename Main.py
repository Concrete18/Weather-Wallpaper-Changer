from Weather_Wallpaper_Changer import Weather
import threading

Main = Weather()
weather_thread = threading.Thread(target=Main.Run, daemon=True)
weather_thread.start()
Main.Create_Tray()
