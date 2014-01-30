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
  Serial1.begin(57600);
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
  Serial1.println("Serial Testing");

}

void loop(){
  cmd = 0;
  cmdstr = "";
  val = 0;
  valstr = "";
  while (Serial1.available() > 0){
    
    char c = Serial1.read();
    readString += c;
  }

  if(readString.length() >= 4){
    cmdstr = readString.substring(0,1);
    valstr = readString.substring(1,4);

    cmd = cmdstr.toInt();
    val = valstr.toInt();

    Serial1.println(cmd);
    Serial1.println(val);

    if(cmd == 0) {
      Serial1.println("STOP");
      //  Serial1.print(String(buf[1]));
      Serial1.println(val);
      analogWrite(10, 148);
      analogWrite(11, 176);
    }
    
    else if(cmd == 2) {
      Serial1.println("X");
	//  Serial1.print(String(buf[1]));
      Serial1.println(val);
      analogWrite(10, val);
    }
      
    else if(cmd ==1){
      Serial1.println("Y");
      //  Serial1.print(String(buf[1]));
      Serial1.println(val);
      analogWrite(11, val);
    }
    else if(cmd == 3){
      Serial1.println("A button");
      Serial1.println(val);
      analogWrite(3, val);
    }
    else if(cmd == 4){
      Serial1.println("X button");
      Serial1.println(val);
      analogWrite(5, val);
    }
    else if(cmd == 5){
      Serial1.println("B button");
      Serial1.println(val);
      analogWrite(6, val);
    }
    else if(cmd == 6){
      Serial1.println("Off");
      Serial1.println(val);
      analogWrite(3, 0);
      analogWrite(5, 0);
      analogWrite(6, 0);
    }
    else {
      analogWrite(10, 148);
      analogWrite(11, 176);
    }
    
    Serial1.println();
    readString="";
  }
}


