//#include <Servo.h>

//Servo servoA;
//Servo servoB;

String readString;
String cmdstr;

String valstr;

int val= 0;
int cmd = 0;

const int xPin = 5;
const int yPin = 4;
const int zPin = 3;

int accminVal = 265;
int accmaxVal = 402;

double x;
double y;
double z;

char sprintbuf [40];

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
  pinMode(9, OUTPUT);
  pinMode(13, OUTPUT);
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
//  servoA.attach(9);
//  servoB.attach(10);
}

void loop(){
  cmd = 0;
  cmdstr = "";
  val = 0;
  valstr = "";
  
    //read the analog values from the accelerometer
  analogReference(EXTERNAL);
  int xRead = analogRead(xPin);
  analogReference(EXTERNAL);
  int yRead = analogRead(yPin);
  analogReference(EXTERNAL);
  int zRead = analogRead(zPin);
  
  int xAng = map(xRead, accminVal, accmaxVal, -90, 90);
  int yAng = map(yRead, accminVal, accmaxVal, -90, 90);
  int zAng = map(zRead, accminVal, accmaxVal, -90, 90);

  //Caculate 360deg values like so: atan2(-yAng, -zAng)
  //atan2 outputs the value of -π to π (radians)
  //We are then converting the radians to degrees
  x = RAD_TO_DEG * (atan2(-yAng, -zAng) + PI);
  y = RAD_TO_DEG * (atan2(-xAng, -zAng) + PI);
  z = RAD_TO_DEG * (atan2(-yAng, -xAng) + PI);
  
  sprintf(sprintbuf, "X:%x  Y:%x  Z:%x", xRead, yRead,zRead);
  Serial1.println(sprintbuf);
//  Serial1.println(xRead);
//  Serial1.println("Y");
//  Serial1.println(yRead);
//  Serial1.println("Z");
//  Serial1.println(zRead);
  
  while (Serial1.available() > 0){
//    delay(1);
    char c = Serial1.read();
    readString += c;
  

  if(c == '\n'){
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
//    else if(cmd == 7){
//      Serial1.println("Servo Y");
//      Serial1.println(val);
//      servoA.write(val);
//    }
//    else if(cmd == 8){
//    Serial1.println("Servo X");
//      Serial1.println(val);
//      servoB.write(val);
//    }
    
    else {
      analogWrite(10, 148);
      analogWrite(11, 176);
    }
    
    Serial1.println();
    readString="";
  }
  }
//readString="";    
}

