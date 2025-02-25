import machine
import time
import network
import dht
import urequests

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("PUSTAKA_106b","bacalah!")

while not wlan.isconnected():
    print(".",end="")
    time.sleep(.1)

print("WLAN is connected")
UBIDOTS_ENDPOINT = "https://industrial.api.ubidots.com/api/v1.6/devices/esp32"
FLASK_ENDPOINT = "http://192.168.19.95:5000/save"


sensor = dht.DHT11(machine.Pin(4))
while True:
    sensor.measure()
    suhu = sensor.temperature()
    kelembaban = sensor.humidity()
    print(f"Suhu = {suhu} C, kelembaban = {kelembaban} %")
    
    data = {"suhu":suhu,"kelembaban":kelembaban}
    headers = {"Content-Type":"application/json","X-Auth-Token":"BBUS-GqHWB1Qhp46sdhZwjA4yHR7zDwnj5I"}
    response = urequests.post(UBIDOTS_ENDPOINT,json=data,headers=headers)
    
    print(f"response ubidots: {response.status_code}")
    response.close()
    
    data = {"suhu":suhu,"kelembaban":kelembaban}
    headers = {"Content-Type":"application/json"}
    response = urequests.post(FLASK_ENDPOINT,json=data,headers=headers,timeout=10)
    
    print(f"response flask: {response.status_code}")
    response.close()
