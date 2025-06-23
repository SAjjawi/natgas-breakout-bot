import websocket
import json

class APIClient:
    def __init__(self):
        self.ws = None
        self.connected = False

    def login(self, user, password, server):
        url = f"wss://ws.{server}.xtb.com/real"
        self.ws = websocket.create_connection(url)
        login_payload = {
            "command": "login",
            "arguments": {"userId": user, "password": password}
        }
        self.ws.send(json.dumps(login_payload))
        resp = json.loads(self.ws.recv())
        if resp["status"]:
            self.connected = True
            print("✅ Login erfolgreich")
        else:
            raise Exception("❌ Login fehlgeschlagen")

    def get_symbol(self, symbol):
        payload = {
            "command": "getTickPrices",
            "arguments": {"symbols": [symbol]}
        }
        self.ws.send(json.dumps(payload))
        resp = json.loads(self.ws.recv())
        data = resp["returnData"][0]
        return {
            "symbol": data["symbol"],
            "ask": float(data["ask"]),
            "bid": float(data["bid"])
        }

    def open_trade(self, trade):
        payload = {
            "command": "tradeTransaction",
            "arguments": trade
        }
        self.ws.send(json.dumps(payload))
        resp = json.loads(self.ws.recv())
        return resp
