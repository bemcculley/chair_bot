// inslude the SPI library:
// #include <SPI.h>


//char buf[100];
String readString;
String cmdstr;
String valstr;

int val= 0;
int cmd = 0;


void setup(){
  //  TCCR1B = TCCR1B & 0b11111000 | 0x01;
  Serial.begin(57600);
  //enable slave mode
  pinMode(3, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  //  pinMode(MISO,OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(4, OUTPUT);
  //  SPCR |= _BV(SPE);


  analogWrite(10, 148);
  analogWrite(11, 176);
  delay(5000);
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
  
  //  SPI.attachInterrupt();
  Serial.println("Serial Testing");

}

void loop(){
  cmd = 0;
  cmdstr = "";
  val = 0;
  valstr = "";
  while (Serial.available() > 0){
    
    char c = Serial.read();
    readString += c;
  }

  if(readString.length() >= 4){
    cmdstr = readString.substring(0,1);
    valstr = readString.substring(1,4);

    cmd = cmdstr.toInt();
    val = valstr.toInt();

    Serial.println(cmd);
    Serial.println(val);

    if(cmd == 0) {
      Serial.println("STOP");
      //  Serial.print(String(buf[1]));
      Serial.println(val);
      analogWrite(10, 148);
      analogWrite(11, 176);
    }
    
    else if(cmd == 2) {
      Serial.println("X");
	//  Serial.print(String(buf[1]));
      Serial.println(val);
      analogWrite(10, val);
    }
      
    else if(cmd ==1){
      Serial.println("Y");
      //  Serial.print(String(buf[1]));
      Serial.println(val);
      analogWrite(11, val);
    }
    else if(cmd == 3){
      Serial.println("A button");
      Serial.println(val);
      analogWrite(3, val);
    }
    else if(cmd == 4){
      Serial.println("X button");
      Serial.println(val);
      analogWrite(5, val);
    }
    else if(cmd == 5){
      Serial.println("B button");
      Serial.println(val);
      analogWrite(6, val);
    }
    else if(cmd == 6){
      Serial.println("Off");
      Serial.println(val);
      analogWrite(3, 0);
      analogWrite(5, 0);
      analogWrite(6, 0);
    }
    else {
      analogWrite(10, 148);
      analogWrite(11, 176);
    }
    
    Serial.println();
    readString="";
  }
}


