import requests
from time import sleep
from datetime import datetime
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD

COLUMNS = 20
SOLAR_MONITOR = "192.168.3.250"
SOLAR_MONITOR_URL = f"http://{SOLAR_MONITOR}/production.json"
lcd = LCD()

def safe_exit(signum, frame):
    exit(1)
    
def power_details():
    solar_response = requests.get(SOLAR_MONITOR_URL,timeout=5)
        
    production = solar_response.json()["production"][1]["wNow"]
    production_data = str(int(round(production,0)))
    consumption = solar_response.json()["consumption"][0]["wNow"]
    consumption_data = str(int(round(consumption,0)))

    consumption_padding = "  "
    if len(consumption_data) > 5:
        consumption_padding = " "
        
    curr_data = f"Now:{consumption_padding}{consumption_data}w"
    curr_padding = " " * (COLUMNS - len(curr_data) - len(production_data + "w"))
    curr_data += curr_padding + production_data + "w"
    
    production_kwh = str(round(solar_response.json()["production"][1]["whToday"]/1000,2))
    consumption_kwh = str(round(solar_response.json()["consumption"][0]["whToday"]/1000,2))
    consumption_kwh_padding = "  "
    if len(consumption_kwh) > 7:
        consumption_kwh_padding = " "
        
    today_data = f"kWh:{consumption_kwh_padding}{consumption_kwh}"
    today_padding = " " * (COLUMNS - len(today_data) - len(production_kwh))
    today_data += today_padding + production_kwh
    
    grid_data = "Usage Gen:"
    net_production = str(round((solar_response.json()["production"][1]["whToday"] - solar_response.json()["consumption"][0]["whToday"])/1000,2))
    grid_padding = " " * (COLUMNS - len(grid_data) - len(net_production))
    grid_data += grid_padding + net_production 
    
    timestamp = datetime.now().strftime("%m/%d/%Y  %H:%M:%S")
    timestamp_padding = " " * (( COLUMNS - len(timestamp)) // 2) 
    timestamp_output = timestamp_padding + timestamp
    
    lcd.text(timestamp_output,1)
    print(timestamp_output)
    
    lcd.text(curr_data, 2)
    print(curr_data)
    
    lcd.text(today_data,3)
    print(today_data)
    
    lcd.text(grid_data,4)
    print(grid_data)

def main():
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)
        while True:
            power_details()
            sleep(10)
    except KeyboardInterrupt:
        pass
    finally:
        lcd.clear()

if __name__ == "__main__":
    main()