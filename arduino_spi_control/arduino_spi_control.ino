// inslude the SPI library:
#include <SPI.h>

char buf[4];
volatile byte pos;
volatile boolean process_it;

//char val[4];
int pwmval= 0;
int pinval= 0;


void setup(){
  TCCR1B = TCCR1B & 0b11111000 | 0x01;
  SPI.setBitOrder(MSBFIRST);
  SPI.setClockDivider(1000000);
  SPI.setDataMode(0);

  Serial.begin(57600);
  //enable slave mode
  pinMode(9, OUTPUT);
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
  delay(5000);
  digitalWrite(4, HIGH);
  analogWrite(9, 255);
  delay(500);
  analogWrite(9, 0);
  analogWrite(6, 255);
  delay(500);
  analogWrite(6, 0);
  analogWrite(5, 255);
  delay(500);
  analogWrite(5, 0);
  analogWrite(6, 58);
  analogWrite(9, 210);
  
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
//  analogWrite(10, 148);
//  analogWrite(11, 176);
//  val[4]="000";
  
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
      analogWrite(9, pinval);
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
      analogWrite(9, 0);
      analogWrite(5, 0);
      analogWrite(6, 0);
    }
    else {
        analogWrite(10, 148);
        analogWrite(11, 176);
    }
    //    for(int i=0;i<4;i++){
    //      xval += buf[
    //      if (buf[i] == 1) {
    //        analogWrite(10, xval);
    //      Serial.print(buf[i],HEX);
    //      Serial.print(" "); 
    Serial.println();
    pos=0;
  }
}


