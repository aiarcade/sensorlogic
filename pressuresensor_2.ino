#include <avr/io.h>
#include <avr/wdt.h>


#define Reset_AVR() wdt_enable(WDTO_30MS); while(1) {}

int sensorValue = 0;        // value read from the pot
int outputValue = 0;        // value output to the PWM (analog out)

int slaverstpin=2;


void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  pinMode(slaverstpin,OUTPUT); 
  digitalWrite(slaverstpin,LOW);
  delay(100);
  digitalWrite(slaverstpin,HIGH);
}

void loop() {
  // read the analog in values:
  char cmd;
      
  int i=1;
  float pressure=0,voltage=0,error=0; 
  if(Serial.available()>0)
  {
    cmd=Serial.read();
    if(cmd=='r')
    {
       Reset_AVR();
       
    }
  } 
    Serial.print("PRS#");

  for(i=1;i<6;i++)
  {
     sensorValue = analogRead(i);            
  // map it to the range of the analog out:
     Serial.print(sensorValue);   
      Serial.print("#");
    // wait 10 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
    delay(10);
  }
  Serial.println("");
  delay(10);
}
  


  

