#include <dht.h>
#include <Wire.h>
#include <Adafruit_BMP085.h>
#include <SoftwareSerial.h>
#include <TinyGPS.h>

#define dht_dpin A0
#define soil_pin A1
#define digital_pin 7

dht DHT;
Adafruit_BMP085 bmp180;

SoftwareSerial mySerial(10, 9);
TinyGPS gps;


long lat, lon;
char control;
int output_value;
int light = 0;

void setup() {
  Serial.begin(9600);
  bmp180.begin();
  mySerial.begin(9600);
  delay(700);
}


void loop() {
     
      if(Serial.available()) {
          control = Serial.read();
          if(control == '1'){
            light = digitalRead(digital_pin);
          switch(light)
          {
            case 0:
            Serial.print("Muita Luz");
            Serial.print(", ");
            break;
            case 1:
            Serial.print("Pouca Luz");
            Serial.print(", ");
            break;
          }
         
          output_value= analogRead(soil_pin);
          output_value = map(output_value,550,0,0,100);
          gps.get_position(&lat, &lon);
          DHT.read11(dht_dpin);
          Serial.print(output_value);
          Serial.print(",");
          Serial.print(DHT.temperature);
          Serial.print(",");
          Serial.print(DHT.humidity);
          Serial.print(",");
          Serial.print(lat); 
          Serial.print(", ");
          Serial.print(lon); 
          Serial.print(", ");
          Serial.print(bmp180.readAltitude());
          Serial.print(", ");
          Serial.print(bmp180.readPressure());  
          Serial.print("\n");    
          
          }
          
      }
}


