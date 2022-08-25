import requests
from datetime import datetime

SOLAR_MONITOR = "192.168.3.250"
SPLUNK_SERVER = "192.168.1.253"
SPLUNK_TOKEN = ""

SOLAR_MONITOR_URL = f"http://{SOLAR_MONITOR}/production.json?details=1"
SPLUNK_HEC_URL = f"http://{SPLUNK_SERVER}:8088/services/collector"


solar_response = requests.get(SOLAR_MONITOR_URL,timeout=5)
splunk_response = requests.post(SPLUNK_HEC_URL,json={"event" : solar_response.json()},headers={"Authorization" : "Splunk {}".format(SPLUNK_TOKEN)},timeout=10)
print("{} - {}".format(datetime.now().isoformat(),splunk_response.content))