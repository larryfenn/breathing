import board
import busio
import time
from digitalio import DigitalInOut
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
from secrets import secrets
import adafruit_scd30
import adafruit_bme680
import adafruit_pm25.i2c
import supervisor

# web connection
server_url = "http://192.168.1.125:5000/sensor"
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
requests.set_socket(socket, esp)

print("Connecting to AP...")

while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except:
        print("Connection error")
        continue
print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)
print("IP address: ", esp.pretty_ip(esp.ip_address))

def web_update():
    aqdata = pm25.read()
    scd_co2 = scd.CO2
    scd_temp = scd.temperature
    scd_hum = scd.relative_humidity
    bme_temp = bme680.temperature
    bme_gas = bme680.gas
    bme_hum = bme680.relative_humidity
    bme_pressure = bme680.pressure
    data = {'password': 'fuck',
    'scd_co2': scd_co2,
    'scd_temp': scd_temp,
    'scd_hum': scd_hum,
    'bme_temp': bme_temp,
    'bme_gas': bme_gas,
    'bme_hum': bme_hum,
    'bme_pressure': bme_pressure,
    'pm25_env': aqdata["pm25 env"],
    'aq_25um': aqdata["particles 25um"]
    }
    # web server also controls whether or not to turn the purifier circuit on or off
    # as the result of the POST request
    return requests.post(url = server_url, data = data)

def purifier_on():
    pass

def purifier_off():
    pass

# sensor board connection
try:
    print("connecting i2c")
    i2c = board.I2C()
    print("connecting SCD30")
    scd = adafruit_scd30.SCD30(i2c)
    print("connecting BME680")
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
    bme680.sea_level_pressure = 1016.26 # only useful to calculate altitude, we don't care about that here
    print("connecting pm25")
    pm25 = adafruit_pm25.i2c.PM25_I2C(i2c)
except Exception as e:
    print(e)
    supervisor.reload()
print("starting loop")

while True:
    try:
        relay_on = web_update().text == "on"
        if(relay_on):
            purifier_on()
        else:
            purifier_off()
        time.sleep(3) # note the SCD30 and PM25 sensors only refresh every 2 seconds or so
    except Exception as e:
        print(e)
        supervisor.reload()
