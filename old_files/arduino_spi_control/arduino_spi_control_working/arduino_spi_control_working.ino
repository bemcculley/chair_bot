// inslude the SPI library:
#include <SPI.h>

char buf[100];
volatile byte pos;
volatile boolean process_it;

char val[4];
int pwmval=0;
int pinval= 0;

const int pingPin = 7;

void setup(){
  TCCR1B = TCCR1B & 0b11111000 | 0x01;
  Serial.begin(57600);
  //enable slave mode
  pinMode(3, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(MISO,OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(4, OUTPUT);
  SPCR |= _BV(SPE);

  //initialize buffer
  pos = 0;

  analogWrite(10, 148);
  analogWrite(11, 176);
  delay(1000);
  digitalWrite(4, HIGH);
  analogWrite(3, 255);
  delay(500);
  analogWrite(3, 0);
  analogWrite(6, 255);
  delay(500);
  analogWrite(6, 0);
  analogWrite(5, 255);
  delay(500);
  analogWrite(5, 0);
  analogWrite(6, 58);
  analogWrite(3, 210);
  
  SPI.attachInterrupt();
  Serial.println("SPI Testing");

}

ISR(SPI_STC_vect)
{
  byte c = SPDR;
  if(pos<sizeof buf)
  {
    buf[pos++]=c;
        //Serial.print(c, HEX);
  }
  //echo incoming byte back out
  SPDR = c;
//  pinval = 0;
}

void loop(){
  SPDR=0;
  pwmval=0;
  pinval=0;


  Serial.println("Loop");
  // establish variables for duration of the ping,
  // and the distance result in inches and centimeters:
  long duration, inches, cm;
  
  // The PING))) is triggered by a HIGH pulse of 2 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  pinMode(pingPin, OUTPUT);
  digitalWrite(pingPin, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(pingPin, LOW);  
  
  // The same pin is used to read the signal from the PING))): a HIGH
  // pulse whose duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode(pingPin, INPUT);
  duration = pulseIn(pingPin, HIGH);

  cm = microsecondsToCentimeters(duration);
  Serial.print("cm: ");Serial.print(cm);Serial.println();
//  if(cm <=  80){
//      analogWrite(10, 148);
//      analogWrite(11, 176);
//      digitalWrite(4, LOW);
//  }  
  
  if(pos==4){
      pinval += buf[1] * 100;
      pinval += buf[2] * 10;
      pinval += buf[3];


    if(buf[0] == 0) {
      Serial.print("STOP");
    //  Serial.print(String(buf[1]));
      Serial.println(pinval);
      analogWrite(10, 148);
      analogWrite(11, 176);
    }
    
    if(buf[0] == 2) {
      Serial.print("X");
    //  Serial.print(String(buf[1]));
      Serial.println(pinval);
      analogWrite(10, pinval);
    }
    
    else if(buf[0] ==1){
      Serial.print("Y");
    //  Serial.print(String(buf[1]));
      Serial.println(pinval);
      analogWrite(11, pinval);
    }
    else if(buf[0] == 3){
      Serial.print("A");
      Serial.print(pinval);
      analogWrite(3, pinval);
    }
    else if(buf[0] == 4){
      Serial.print("X");
      Serial.print(pinval);
      analogWrite(5, pinval);
    }
    else if(buf[0] == 5){
      Serial.print("B");
      Serial.print(pinval);
      analogWrite(6, pinval);
    }
    else if(buf[0] == 6){
      Serial.print("Off");
      Serial.print(pinval);
      analogWrite(3, 0);
      analogWrite(5, 0);
      analogWrite(6, 0);
    }
    else {
        analogWrite(10, 148);
        analogWrite(11, 176);
    }

    Serial.println();
    pos=0;
  }

}

long microsecondsToCentimeters(long microseconds)
{
  // The speed of sound is 340 m/s or 29 microseconds per centimeter.
  // The ping travels out and back, so to find the distance of the
  // object we take half of the distance travelled.
  return microseconds / 29 / 2;
}


