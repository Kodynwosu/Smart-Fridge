import tkinter as tk
import requests

def fetch_current_weather(city):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={city['latitude']}&longitude={city['longitude']}&current_weather=true"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and 'current_weather' in data:
        temperature = data['current_weather']['temperature']
        weather_code = data['current_weather']['weathercode']
        return temperature, get_weather_icon(weather_code)
    else:
        return None, None

def get_weather_icon(weather_code):
    """Returns colorful weather icons based on weather codes."""
    if weather_code == 0:
        return "☀️ Sunny"
    elif weather_code in [1, 2]:
        return "🌤️ Partly Cloudy"
    elif weather_code in [3, 4]:
        return "☁️ Cloudy 🌥️"
    elif weather_code in [5, 6, 7]:
        return "🌧️ Rainy 🌦️"
    elif weather_code in [8, 9]:
        return "❄️ Snowy ☃️"
    elif weather_code >= 10:
        return "⛈️ Stormy ⚡"
    else:
        return "🌈 Mixed Weather"

def update_weather_display():
    weather_display = []
    for city_name, city_coords in cities.items():
        temperature, icon = fetch_current_weather(city_coords)
        if temperature is not None:
            weather_display.append(f"{city_name}: {temperature}°C  {icon}")
        else:
            weather_display.append(f"{city_name}: Weather data not available.")
    weather_label.config(text="\n".join(weather_display))

def fetch_news():
    api_key = "8575888e32f64b51acef22480bc279c0"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and "articles" in data:
        headlines = []
        for article in data["articles"][:5]:  # Get the first 5 articles
            headlines.append(f"- {article['title']}")
        return headlines
    else:
        return ["Unable to fetch news."]

def update_news_display():
    headlines = fetch_news()
    news_label.config(text="\n".join(headlines))

def fetch_football_scores():
    api_key = "9155a3b241044a32b86230972e663c0c"
    url = "https://api.football-data.org/v4/matches"
    headers = {"X-Auth-Token": api_key}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if response.status_code == 200 and "matches" in data:
            scores = []
            for match in data["matches"][:5]:  # Get the first 5 matches
                home_team = match["homeTeam"]["name"]
                away_team = match["awayTeam"]["name"]
                home_score = match["score"]["fullTime"].get("home", 0)
                away_score = match["score"]["fullTime"].get("away", 0)
                scores.append(f"{home_team} {home_score} - {away_score} {away_team}")
            return scores
        elif response.status_code == 401:
            return ["Invalid API Key. Please check your key."]
        elif response.status_code == 404:
            return ["No matches found for the specified criteria."]
        else:
            return [f"Error: Unable to fetch football scores."]
    except Exception as e:
        return [f"Error: Unable to fetch football scores due to {str(e)}."]

def update_football_scores_display():
    scores = fetch_football_scores()
    football_scores_label.config(text="\n".join(scores))

cities = {
    "Toronto": {"latitude": 43.65107, "longitude": -79.347015},
    "Vancouver": {"latitude": 49.282729, "longitude": -123.120738},
    "Montreal": {"latitude": 45.501689, "longitude": -73.567256},
    "Ottawa": {"latitude": 45.421532, "longitude": -75.697189},
    "Calgary": {"latitude": 51.044733, "longitude": -114.071883},
    "Beamsville": {"latitude": 43.1656, "longitude": -79.4829}
}

root = tk.Tk()
root.title("Dashboard")
root.geometry("1000x600")
root.configure(bg="#E8F4FD")

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)

weather_frame = tk.Frame(root, bg="#ADD8E6", padx=10, pady=10)
weather_frame.grid(row=0, column=0, sticky="nsew")
weather_title = tk.Label(weather_frame, text="Weather Forecast", font=("Helvetica", 18, "bold"), bg="#ADD8E6")
weather_title.pack()
weather_label = tk.Label(weather_frame, font=("Helvetica", 14), bg="#ADD8E6", justify="left", wraplength=400)
weather_label.pack()
update_weather_display()

news_frame = tk.Frame(root, bg="#87CEEB", padx=10, pady=10)
news_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")
news_title = tk.Label(news_frame, text="Top News Headlines", font=("Helvetica", 18, "bold"), bg="#87CEEB")
news_title.pack()
news_label = tk.Label(news_frame, font=("Helvetica", 16), bg="#87CEEB", justify="left", wraplength=400)
news_label.pack()
update_news_display()

football_frame = tk.Frame(root, bg="#4682B4", padx=10, pady=10)
football_frame.grid(row=1, column=0, sticky="nsew")
football_title = tk.Label(football_frame, text="Football Scores", font=("Helvetica", 18, "bold"), bg="#4682B4", fg="white")
football_title.pack()
football_scores_label = tk.Label(football_frame, font=("Helvetica", 14), bg="#4682B4", fg="white", justify="left")
football_scores_label.pack()
update_football_scores_display()

root.mainloop()


