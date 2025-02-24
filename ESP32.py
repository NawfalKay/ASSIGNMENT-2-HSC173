import network
import urequests
import json
from machine import Pin
import dht
import time

WIFI_SSID = "NAMA_WIFI"
WIFI_PASS = "PASSWORD_WIFI"

UBIDOTS_TOKEN = "TOKEN_UBIDOTS"
DEVICE_LABEL = "esp32"
UBIDOTS_URL = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}"

FLASK_API_URL = "http://IP_SERVER:5000/data"

dht_sensor = dht.DHT11(Pin(4))
TRIGGER_PIN = 5
ECHO_PIN = 18
trigger = machine.Pin(TRIGGER_PIN, machine.Pin.OUT)
echo = machine.Pin(ECHO_PIN, machine.Pin.IN)

def ukur_jarak():
    trigger.low()
    time.sleep_us(2)
    trigger.high()
    time.sleep_us(10)
    trigger.low()
    while echo.value() == 0:
        pass
    start = time.ticks_us()
    while echo.value() == 1:
        pass
    end = time.ticks_us()
    duration = time.ticks_diff(end, start)
    jarak = (duration * 0.0343) / 2
    return jarak

def baca_dht11():
    dht_sensor.measure()
    return dht_sensor.temperature(), dht_sensor.humidity()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    wlan.connect(WIFI_SSID, WIFI_PASS)
    while not wlan.isconnected():
        pass
print("IP:", wlan.ifconfig()[0])

def kirim_ke_ubidots(jarak, suhu, kelembaban):
    headers = {"X-Auth-Token": UBIDOTS_TOKEN, "Content-Type": "application/json"}
    data = {"jarak": jarak, "suhu": suhu, "kelembaban": kelembaban}
    try:
        response = urequests.post(UBIDOTS_URL, headers=headers, json=data)
        print("Ubidots Response:", response.text)
        response.close()
    except Exception as e:
        print("Error Ubidots:", e)

def kirim_ke_flask(jarak, suhu, kelembaban):
    data = {"sensor": "ultrasonic_dht11", "jarak": jarak, "suhu": suhu, "kelembaban": kelembaban}
    try:
        response = urequests.post(FLASK_API_URL, json=data)
        print("Flask Response:", response.text)
        response.close()
    except Exception as e:
        print("Error Flask API:", e)

while True:
    jarak = ukur_jarak()
    suhu, kelembaban = baca_dht11()
    print("Jarak:", jarak, "cm | Suhu:", suhu, "°C | Kelembaban:", kelembaban, "%")
    kirim_ke_ubidots(jarak, suhu, kelembaban)
    kirim_ke_flask(jarak, suhu, kelembaban)
    time.sleep(5)