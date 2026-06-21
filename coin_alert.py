python
import requests
import os

# 환경변수에서 토큰/ID 불러오기 (보안을 위해 코드에 직접 안 적음)
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

# 알림받고 싶은 코인 (업비트 마켓 코드 기준)
COINS = {
    "KRW-BTC": "비트코인",
    "KRW-ETH": "이더리움",
    "KRW-ONDO": "온도파이낸스",
    "KRW-ENS": "이더리움네임서비스",
}

def get_prices():
    markets = ",".join(COINS.keys())
    url = f"https://api.upbit.com/v1/ticker?markets={markets}"
    res = requests.get(url).json()
    return res

def format_message(data):
    lines = ["📊 코인 시세 알림\n"]
    for item in data:
        market = item["market"]
        name = COINS.get(market, market)
        price = item["trade_price"]
        change_rate = item["signed_change_rate"] * 100
        change_emoji = "🔺" if change_rate >= 0 else "🔻"
        lines.append(f"{name}: {price:,.0f}원 {change_emoji} {change_rate:+.2f}%")
    return "\n".join(lines)

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    res = requests.post(url, data=payload)
    print(res.status_code, res.text)

if __name__ == "__main__":
    data = get_prices()
    message = format_message(data)
    send_telegram(message)
