from datetime import datetime, time
import time as t
import mysql.connector
import serial
import sched


ser = serial.Serial('/dev/ttyACM0', 9600)

cnx = mysql.connector.connect(user='root', password='raspberry',
				host='127.0.0.1',
				database='Greenhouse')
cursor = cnx.cursor()

now = datetime.now()

light = ""
moisture = ""
humidity = ""
temperature = ""
lightvalue = 0
moisturevalue = 0
humidityvalue = 0
temperaturevalue = 0
temperaturevalue = 0

FanOff = "Fan: 0\n"
FanOn = "Fan: 1\n"
PumpOff = "Pump: 0\n"
PumpOn = "Pump: 1\n"
LightOff = "Light: 0\n"
LightOn = "Light: 1\n"

isWatering = False
isFanOn = False

isLampOn = False

def insert_to_database(sc):
	#print lightvalue
	#print moisturevalue
	#print humidityvalue
	#print temperaturevalue
	insert_stmt =(
			"INSERT INTO Greenhouse.measurements (light, soil_moist, air_humidity, air_temp) "
			"VALUES (%s, %s, %s, %s)"
			)
	data = (lightvalue, moisturevalue, humidityvalue, temperaturevalue)
	cursor.execute(insert_stmt, data)
       # Makes sure data is commited to DB 
	cnx.commit()
	print "databaseinsertion"
	s.enter(60, 2, insert_to_database, (sc,))

def pumpburst(sc):
	global isWatering
	isWatering = True
	ser.write(PumpOn)
	print "pumpON"
	s.enter(0.75, 1, setPumpOff, (sc,))
	
def setPumpOff(sc):
	ser.write(PumpOff)
	print "pumpOFF"
	s.enter(10,1, setWateringOff, (sc,))
	
def setWateringOff(sc):
	print "wateringOff"
	global isWatering
	isWatering = False

def turnOnLamp():
	ser.write(LightOn)
	
def turnOffLamp():
	ser.write(LightOff)
	
def checkTime(sc):
	#LightTimeStart = timeNow.replace(hour=8, minute=0, seconds=0)
	#LightTimeEnd = timeNow.replace(hour=16, minute=0, seconds=0)
	now_time = datetime.now().time()
	
	#print type(str(now_time))
	print "time: " + str(now_time)
	print light + moisture + humidity + temperature
	global isLampOn
	if(now_time >= time(9,00) and now_time < time(16,00) and not(isLampOn)):
		print "lampOn"
		isLampOn = True
		turnOnLamp()
	elif(not(now_time >= time(9,00) and now_time < time(16,00)) and isLampOn):
		print "lampOff"
		isLampOn = False
		turnOffLamp()
		
	s.enter(1, 2, checkTime, (sc,))

def main_prog(sc):
	inputstring =ser.readline()
	#print inputstring
	validString = inputstring.find("L:")!=-1 and inputstring.find("M:")!=-1 and inputstring.find("H:")!=-1 and inputstring.find("T:")!=-1
	
	if(inputstring.count("\t")==3 and validString):
		splitted = inputstring.split("\t",3)
		if(len(splitted)==4):
			global light
			global moisture
			global humidity
			global temperature
			global lightvalue
			global moisturevalue
			global humidityvalue
			global temperaturevalue
			light = splitted[0]
			moisture = splitted[1]
			humidity = splitted[2]
			temperature = splitted[3]
			lightvalue = splitted[0].split("L:",1)[1]
			moisturevalue = splitted[1].split("M:",1)[1]
			humidityvalue = splitted[2].split("H:",1)[1]
			temperaturevalue = splitted[3].split("T:",1)[1]
			temperaturevalue = temperaturevalue.split("\r\n",1)[0]
			
			#print lightvalue
			#print moisturevalue
			#print humidityvalue
			#print temperaturevalue

			
	               #temperture : Fan on and off
			isTempToHigh = (float(temperaturevalue)>26)
			global isFanOn
			if(isTempToHigh and not(isFanOn)):
				
				isFanOn = True
				ser.write(FanOn)
			elif(not (isTempToHigh) and isFanOn):
				isFanOn = False
				ser.write(FanOff)
			#pump: moisture 0-600
			
			moistureToLow = (int(moisturevalue)>100)
			global isWatering
			if((moistureToLow) and not(isWatering)):
				
				isWatering = True
				s.enter(0,1,pumpburst, (sc,))

			
	s.enter(0, 4, main_prog, (s,))

        	        #send On Off Information to DB

                
s = sched.scheduler(t.time, t.sleep)
s.enter(8, 4, main_prog, (s,))
s.enter(10, 2, checkTime, (s,))
s.enter(15, 3, insert_to_database, (s,))

s.run()		
		#t.sleep(1)	

#cursor.close()
#cnx.close()
	



#cnx = mysql.connector.connect(user='root', password='raspberry',
#				host='127.0.0.1',
#				database='Greenhouse')

#cursor = cnx.cursor()

#cursor.execute("SELECT * FROM measurements LIMIT 1")





#cnx.commit()


cursor.close()
cnx.close()
