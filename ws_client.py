import websocket
import argparse
import json

def on_message(ws, message):
    print(f"Received message: {message}")

def on_error(ws, error):
    print(f"Encountered error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

def on_open(ws):
    print("Connection opened")
    ws.send(json.dumps({'subscribe': f"/sites/{args.site_id}/devices/{args.device_id}/cmd"}))

parser = argparse.ArgumentParser()
parser.add_argument('-topic')
parser.add_argument('-site_id')
parser.add_argument('-device_id')
args = parser.parse_args()

token="ASostdRKz4TsmKfoiwEEN4deFSLCehuwFWhfDuJlQp0JOD7f8CMeLurUWIfzYCazIZdKESb2i5Dgsg526xrLmWdSTTEva0O5"
header = [f"Authorization: Bearer {token}"]
ws = websocket.WebSocketApp("ws://api-ws.mist.com/v1/stream",
                            header=header,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.on_open = on_open
ws.run_forever()