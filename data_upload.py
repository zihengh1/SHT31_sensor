import smbus
import sys  
import time  
import httplib, urllib  

sys.path.append('/home/pi/rpi/i2c_sensor_test')  

#**************************************************** 
# Set Pin No, ThingSpeak Key                                                                          
#**************************************************** 

sensor = 4  
blue = 0    # The Blue colored sensor.  
white = 1   # The White colored sensor.
thingSpeakApiKey = "EQFAFGEN2J94AMTM"

#**************************************************** 
# Set ThingSpeak Connection                                                   
#**************************************************** 

def post_to_thingspeak(payload):  
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    not_connected = 1
    while (not_connected):
        try:
            conn = httplib.HTTPConnection("api.thingspeak.com:80")
            conn.connect()
            not_connected = 0
        except (httplib.HTTPException, socket.error) as ex:
            print "Error: %s" % ex
            time.sleep(10)  # sleep 10 seconds

    conn.request("POST", "/update", payload, headers)
    response = conn.getresponse()
    print( response.status, response.reason, payload, time.strftime("%c"))
    data = response.read()
    conn.close()

#**************************************************** 
# Post ThingSpeak                                                  
#**************************************************** 
def main():
		while 1:  
				#get i2c bus
				bus = smbus.SMBus(1)
		
				bus.write_i2c_block_data(0x45, 0x2C, [0x06])
				time.sleep(0.5)
				data = bus.read_i2c_block_data(0x45, 0x00, 6)

				temp = data[0] * 256 + data[1]
				cTemp = -45 + (175 * temp / 65535.0)
				fTemp = -49 + (315 * temp / 65535.0)
				humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

				print "Celsius : %.2f C" %cTemp
				print "Fahrenheit : %.2f F" %fTemp
				print "Humidity : %.2f %%RH" %humidity
		
				bus.close()
				params = urllib.urlencode({'field1': cTemp, 'field2': fTemp, 'field3': humidity, 'key': thingSpeakApiKey})

				post_to_thingspeak(params)
				time.sleep(5)

if __name__ == "__main__":
    main()

