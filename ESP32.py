import machine
import time
import network
import dht
import urequests

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("PUSTAKA_106b", "bacalah!")

buzzer = machine.Pin(2, machine.Pin.OUT)

def beep(times, duration=0.2, interval=0.2):

    for _ in range(times):
        buzzer.on()
        time.sleep(duration)
        buzzer.off()
        time.sleep(interval)

while not wlan.isconnected():
    print(".", end="")
    time.sleep(0.1)

print("WLAN is connected")
beep(2)
UBIDOTS_ENDPOINT = "https://industrial.api.ubidots.com/api/v1.6/devices/esp32"
FLASK_ENDPOINT = "http://192.168.19.95:5000/save"

sensor_dht = dht.DHT11(machine.Pin(4))

TRIG = machine.Pin(5, machine.Pin.OUT)
ECHO = machine.Pin(18, machine.Pin.IN)

def get_distance():
    TRIG.off()
    time.sleep_us(2)
    TRIG.on()
    time.sleep_us(10)
    TRIG.off()

    while ECHO.value() == 0:
        start_time = time.ticks_us()

    while ECHO.value() == 1:
        end_time = time.ticks_us()

    duration = end_time - start_time
    distance = (duration * 0.0343) / 2
    return distance

while True:
    sensor_dht.measure()
    suhu = sensor_dht.temperature()
    kelembaban = sensor_dht.humidity()
    
    jarak = get_distance()

    print(f"Suhu = {suhu} C, Kelembaban = {kelembaban} %, Jarak = {jarak:.2f} cm")
    
  
    data = {"suhu": suhu, "kelembaban": kelembaban, "jarak": jarak}
    headers = {"Content-Type": "application/json", "X-Auth-Token": "BBUS-GqHWB1Qhp46sdhZwjA4yHR7zDwnj5I"}

    try:
        response = urequests.post(UBIDOTS_ENDPOINT, json=data, headers=headers)
        print(f"response ubidots: {response.status_code}")
        response.close()

        response = urequests.post(FLASK_ENDPOINT, json=data, headers={"Content-Type": "application/json"}, timeout=10)
        print(f"response flask: {response.status_code}")
        response.close()

        beep(1, 0.5) 

    except Exception as e:
        print("Gagal mengirim data:", e)

    time.sleep(5)

