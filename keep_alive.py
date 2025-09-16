# keep_alive.py
import time
import requests

URL = "https://carpricefastapi.onrender.com/"

while True:
    try:
        r = requests.get(URL, timeout=10)
        print(f"Pinged {URL}, status: {r.status_code}")
    except Exception as e:
        print(f"Error pinging {URL}: {e}")
    time.sleep(300)  # wait 5 minutes
