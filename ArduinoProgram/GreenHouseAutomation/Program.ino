// Example testing sketch for various DHT humidity/temperature sensors
// Written by ladyada, public domain

#include "DHT.h"

#define DHTPIN 2     // what digital pin we're connected to

int sensorvalueLight = 0;
int sensorvalueMoisture =0;
int relayTestPin = 8;
int pumpControlPin = 3;
int fanControlPin = 4;
int lightControlPin = 5;

// Uncomment whatever type you're using!
#define DHTTYPE DHT11   // DHT 11
//define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

// Connect pin 1 (on the left) of the sensor to +5V
// NOTE: If using a board with 3.3V logic like an Arduino Due connect pin 1
// to 3.3V instead of 5V!
// Connect pin 2 of the sensor to whatever your DHTPIN is
// Connect pin 4 (on the right) of the sensor to GROUND
// Connect a 10K resistor from pin 2 (data) to pin 1 (power) of the sensor

// Initialize DHT sensor.
// Note that older versions of this library took an optional third parameter to
// tweak the timings for faster processors.  This parameter is no longer needed
// as the current DHT reading algorithm adjusts itself to work on faster procs.
DHT dht(DHTPIN, DHTTYPE);

String str;

String FanOff = "Fan: 0";
String FanOn = "Fan: 1";
String PumpOff = "Pump: 0";
String PumpOn = "Pump: 1";
String LightOff = "Light: 0";
String LightOn = "Light: 1";

void setup() {
  Serial.println("Starting program!");
  Serial.begin(9600);
  pinMode(pumpControlPin, OUTPUT);
  pinMode(fanControlPin, OUTPUT);
  pinMode(lightControlPin, OUTPUT);
  
  
  dht.begin();
}

int compare(String str, String cmp)
{
  
  if(str.equals(cmp)){
    return 1; 
  }
  else{
    return 0;
  }
}

void readSerial() {
    while (Serial.available() > 0) // Don't read unless
    {                               // there you know there is data
        str = Serial.readStringUntil('\n');
        //Serial.print(str);
        if(compare(str, FanOff))
        {
          digitalWrite(fanControlPin, LOW);
          //Serial.write("Fan Off \n"); 
        }
        else if(compare(str, FanOn))
        {
          digitalWrite(fanControlPin, HIGH);
          //Serial.write("Fan On \n");
          }
        else if(compare(str, PumpOff))
        {
          digitalWrite(pumpControlPin, LOW);
          //Serial.write("Pump Off \n");
        }
        else if(compare(str, PumpOn))
        {
          digitalWrite(pumpControlPin, HIGH);
          //Serial.write("Pump On \n");  
        }
        else if(compare(str, LightOff))
        {
          digitalWrite(lightControlPin, LOW);
          //Serial.write("Light Off \n");
        }
        else if(compare(str, LightOn))
        {
          digitalWrite(lightControlPin, HIGH);
          //Serial.write("Light On \n");
        }
        
    }
}

void loop() {
  // Wait a few seconds between measurements.

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  sensorvalueLight = analogRead(A0);  //Read the light sensor analog value
  sensorvalueMoisture = analogRead(A1);  //Read the moisture sensor analog value
  Serial.print("L:");  
  Serial.print(sensorvalueLight);  //Print the analog value
  Serial.print("\tM:");  
  Serial.print(sensorvalueMoisture);  //Print the analog value
  
  Serial.print("\tH:");
  Serial.print(h);
  Serial.print("\tT:");
  Serial.print(t);
  Serial.print("\r\n");

  readSerial();
}



