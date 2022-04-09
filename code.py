import time
import board
import adafruit_scd30
import adafruit_bme680
from adafruit_pm25.i2c import PM25_I2C

# Initialization step 1: sensor connections

i2c = board.I2C()
scd = adafruit_scd30.SCD30(i2c)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
bme680.sea_level_pressure = 1016.26 # sea level - make this update from web server later
pm25 = PM25_I2C(i2c)

# Initialization step 2: server connection

# basically, connect to a LAN web server which will log data and pull latest sea level pressure data
# web server also controls whether or not to turn the purifier circuit on or off

# Initialization step 3 (?): BME 688 calibration

while True:
    # since the measurement interval is long (2+ seconds) we check for new data before reading
    # the values, to ensure current readings.
    if scd.data_available:
        aqdata = pm25.read()
        print("Data Available!")
        print("CO2:", scd.CO2, "PPM")
        print("Temperature:", scd.temperature, "degrees C")
        print("Humidity:", scd.relative_humidity, "%%rH")
        print("\nTemperature: %0.1f C" % bme680.temperature)
        print("Gas: %d ohm" % bme680.gas)
        print("Humidity: %0.1f %%" % bme680.relative_humidity)
        print("Pressure: %0.3f hPa" % bme680.pressure)
        print("Altitude = %0.2f meters" % bme680.altitude)
        print("Concentration Units (standard)")
        print("---------------------------------------")
        print(
            "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
            % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
        )
        print("Concentration Units (environmental)")
        print("---------------------------------------")
        print(
            "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
            % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
        )
        print("---------------------------------------")
        print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
        print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
        print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
        print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
        print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
        print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
        print("---------------------------------------")
        print("")
        print("Waiting for new data...")
        print("")

    time.sleep(0.5)

# necessary helper functions

def sensor_read():

def web_update():

def purifier_on():

def purifier_off():

def calibrate():
