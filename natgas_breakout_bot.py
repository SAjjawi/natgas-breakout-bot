from xAPIConnector import APIClient
from config import *
import time, datetime, requests

client = APIClient()
client.login(XTB_USER_ID, XTB_PASSWORD, XTB_SERVER)

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram-Fehler:", e)

def open_trade(trade_type, price, sl, tp):
    trade = {
        "symbol": NATGAS_SYMBOL,
        "volume": 0.1,
        "cmd": 0 if trade_type == "buy" else 1,
        "price": price,
        "sl": sl,
        "tp": tp,
        "type": 0,
        "customComment": "BreakoutBot"
    }
    response = client.open_trade(trade)
    send_telegram(f"🚨 {trade_type.upper()} @ {price} | TP: {tp} / SL: {sl}")
    print("📈 Trade gesendet:", response)

print("🤖 NATGAS BreakoutBot läuft...")

breakout_long = 4.00
breakout_short = 3.85
confirmation_gap = 0.02  # Rücklauf muss passieren
trade_opened = False

while not trade_opened:
    data = client.get_symbol(NATGAS_SYMBOL)
    ask = data["ask"]
    bid = data["bid"]
    print(f"[{datetime.datetime.now()}] ASK: {ask} / BID: {bid}")

    # Long Breakout + Rücklauf
    if ask > breakout_long:
        print("📊 Breakout LONG erkannt")
        time.sleep(20)
        data2 = client.get_symbol(NATGAS_SYMBOL)
        if data2["ask"] < breakout_long + confirmation_gap:
            open_trade("buy", ask, round(ask - 0.10, 3), round(ask + 0.20, 3))
            trade_opened = True

    # Short Breakout + Rücklauf
    elif bid < breakout_short:
        print("📊 Breakout SHORT erkannt")
        time.sleep(20)
        data2 = client.get_symbol(NATGAS_SYMBOL)
        if data2["bid"] > breakout_short - confirmation_gap:
            open_trade("sell", bid, round(bid + 0.10, 3), round(bid - 0.20, 3))
            trade_opened = True

    time.sleep(30)
