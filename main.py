<<<<<<< HEAD
# main.py
# 一時停止用のダミーコード

print("Botは一時停止中です。")
=======
import requests
from datetime import datetime

# --- あなたの設定（実データで置換済） ---
LINE_ACCESS_TOKEN = 'QgHGfokoTBC9Zm8awXgPUN2O0nYduQ4Tq53rhKOWNwGC0+Fk7sy8nycfz8u6RoxMFBJeuJRATPErGNFrcQbF1B+4tfs9nFy3g8U5Rmwh+ffQY4aa4s1XVN7KMUyxSt8dHus1xu3vTrPzdPSjBH73hwdB04t89/1O/w1cDnyilFU='
USER_ID = 'U7b0b2d0689901f95f42f822f5b94d5e1'
OPENWEATHER_API_KEY = '16998bf86c89f7d0d25dca04ccea5411'

LAT = 35.7388  # 緯度：石神井公園
LON = 139.5862  # 経度：石神井公園

# --- 天気アイコン辞書 ---
WEATHER_ICONS = {
    'clear': '☀️',
    'clouds': '☁️',
    'rain': '🌧️',
    'drizzle': '🌦️',
    'thunderstorm': '⛈️',
    'snow': '❄️',
    'mist': '🌫️'
}

# --- 天気メッセージ生成 ---
def get_weather_message():
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={OPENWEATHER_API_KEY}&lang=ja&units=metric'
    res = requests.get(url).json()

    if res.get("cod") != "200":
        return "天気情報を取得できませんでした。"

    forecasts = res['list'][:8]  # 3時間ごと×8 = 24時間分
    lines = []
    temps = []
    needs_umbrella = False

    for f in forecasts:
        dt = datetime.fromtimestamp(f['dt'])
        time_str = dt.strftime('%H:%M')
        weather_main = f['weather'][0]['main'].lower()
        weather_desc = f['weather'][0]['description']
        temp = f['main']['temp']
        temps.append(temp)

        icon = WEATHER_ICONS.get(weather_main, '')
        lines.append(f"{time_str} {icon} {weather_desc} {temp:.1f}℃")

        if '雨' in weather_desc and '霧' not in weather_desc:
            needs_umbrella = True

    min_temp = min(temps)
    max_temp = max(temps)

    message = f"【石神井公園付近の天気（24時間分）】\n"
    message += f"最低気温：{min_temp:.1f}℃\n最高気温：{max_temp:.1f}℃\n"
    if needs_umbrella:
        message += "☔ 傘を忘れずに！\n"
    message += "\n".join(lines)

    return message

# --- LINE通知関数 ---
def send_line_message(user_id, message):
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
    }
    data = {
        'to': user_id,
        'messages': [{'type': 'text', 'text': message}]
    }
    response = requests.post(url, headers=headers, json=data)
    print(f'送信結果: {response.status_code} / {response.text}')

# --- 実行部 ---
if __name__ == '__main__':
    message = get_weather_message()
    send_line_message(USER_ID, message)
>>>>>>> 986a199edf212d4080110f968b7a123d64e45dfe
