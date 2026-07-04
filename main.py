import os
import requests
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

def load_env(path=".env"):
  if not os.path.exists(path):
    return
  with open(path, "r", encoding="utf-8") as env_file:
    for line in env_file:
      line = line.strip()
      if not line or line.startswith("#") or "=" not in line:
        continue
      key, value = line.split("=", 1)
      key = key.strip()
      value = value.strip().strip('"').strip("'")
      if key and key not in os.environ:
        os.environ[key] = value


def get_image():
  global img, image_Label
  icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"
  response = requests.get(icon_url)
  image = Image.open(BytesIO(response.content))
  img = ImageTk.PhotoImage(image)
  image_Label.config(image=img)
  image_Label.pack(side = "bottom", fill = "both", expand = "yes")


def get_weather():
  global icon
  city = city_entry.get().strip()
  api_key = os.getenv("OPENWEATHER_API_KEY")
  if not api_key:
    result_Label.config(text="OPENWEATHER_API_KEY environment variable is not set.")
    return
  weather = requests.get(
    "https://api.openweathermap.org/data/2.5/weather",
    params={"q": city, "units": "imperial", "APPID": api_key},
  )
  data = weather.json()
  if weather.status_code == 404 or data.get("cod") == "404":
    result_Label.config(text=f"No city found with the name {city}")
    return
  result_Label.config(text=f"the weather in {city} is {data['weather'][0]['description']} with a temperature of {data['main']['temp']} degrees Fahrenheit")
  icon = data["weather"][0]["icon"]
  get_image()    


load_env()

pinecone = tk.Tk()
pinecone.title("Weather App")
tk.Label(pinecone, text="Enter a city").pack()
city_entry = tk.Entry(pinecone)
city_entry.pack()
tk.Button(pinecone, text="Get Weather", command=get_weather).pack()
image_Label = tk.Label(pinecone)
image_Label.pack_forget()
result_Label = tk.Label(pinecone, text="result")
result_Label.pack()
pinecone.mainloop()