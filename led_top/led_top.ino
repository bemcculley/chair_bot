#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>
#endif

#define PIN 4
String mode = "off";

// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(136, PIN, NEO_GRB + NEO_KHZ800);



const char* ssid = "doomngloom";
const char* password = "rossperotsdirtylittlesecret";

ESP8266WebServer server(80);

const int led = 5;
int animate = 0;
int animate_wait = 100;
int red = 0;
int green = 0;
int blue = 0;

void handleRoot() {
  digitalWrite(led, 1);
  server.send(200, "text/plain", "hello from esp8266!");
  digitalWrite(led, 0);
}

void handleOff() {
  mode = "off";
  server.send(200, "text/plain", "Leds Off");
}


void handleOn() {
  mode = "on";
  server.send(200, "text/plain", "Leds On");
}

void handleAnimate() {
  String message = "";

  if (server.arg("animate") == "") {   //Parameter not found
    message = "Animate Argument not found";
    mode = "off";
  } else {
     //Parameter found
    animate = server.arg("animate").toInt(); //Gets the value of the query parameter
    message = "Animate Argument = ";
    message += server.arg("animate");
    message += "\n"; 
    mode = "on";
    if (server.arg("delay") == ""){
      animate_wait = 100;
    } else {
      animate_wait = server.arg("delay").toInt();
    }
  }
  server.send(200, "text/plain", message);
}

void handleColor() {
  mode = "on";
  String message = "";
  if (server.arg("red") == "") {   //Parameter not found
    message = "red Argument not found";
  } else {
    animate = 12;
     //Parameter found
    red = constrain(server.arg("red").toInt(), 0, 255); //Gets the value of the query parameter
    message = "red Argument = ";
    message += server.arg("red");
    message += "\n"; 
  }
  if (server.arg("green") == "") {   //Parameter not found
    message += "green Argument not found";
  } else {
    animate = 12;
     //Parameter found
    green = constrain(server.arg("green").toInt(), 0, 255); //Gets the value of the query parameter
    message += "green Argument = ";
    message += server.arg("green");
    message += "\n";
  }
  if (server.arg("blue") == "") {   //Parameter not found
    message += "blue Argument not found";
  } else {
    animate = 12;
     //Parameter found
    blue = constrain(server.arg("blue").toInt(), 0, 255); //Gets the value of the query parameter
    message += "blue Argument = ";
    message += server.arg("blue");
    message += "\n";
  }
  server.send(200, "text/plain", message);
}

void handleNotFound() {
  digitalWrite(led, 1);
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
  digitalWrite(led, 0);
}

void setup(void) {
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
  pinMode(led, OUTPUT);
  digitalWrite(led, 0);
  Serial.begin(115200);

    // config static IP
  IPAddress ip(192, 168, 42, 2);
  IPAddress gateway(192, 168, 42, 1);
  Serial.print(F("Setting static ip to : "));
  Serial.println(ip);
  IPAddress subnet(255, 255, 255, 0); 
  WiFi.config(ip, gateway, subnet);
  WiFi.begin(ssid, password);
  Serial.println("");


  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("tv_leds")) {
    Serial.println("MDNS responder started");
  }

  for (uint16_t i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, strip.Color(255, 0, 255));
  }
  strip.show();

  server.on("/", handleRoot);
  server.on("/off", handleOff);
  server.on("/on", handleOn);
  server.on("/led", handleAnimate);
  server.on("/color", handleColor);
  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
  boot();
}

void loop(void) {
  server.handleClient();
  if (mode == "off"){
    for (uint16_t i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, strip.Color(0, 0, 0));
    } 
  strip.show();
  }
  if (mode == "on"){
    if (animate == 1){
      rainbowCycle(animate_wait);
    }
  }
  if (mode == "on"){
    if (animate == 2){
      chase(strip.Color(255, 0, 0)); // Red
    }
  }
  if (mode == "on"){
    if (animate == 3){
      chase(strip.Color(0, 255, 0)); // Green
    }
  }
  if (mode == "on"){
    if (animate == 4){
      chase(strip.Color(0, 0, 255)); // Blue
    }
  }
  if (mode == "on"){
    if (animate == 5){
      police(animate_wait);
    }
  }
  if (mode == "on"){
    if (animate == 6){
      police2(animate_wait);
    }
  }
  if (mode == "on"){
    if (animate == 7){
      for (uint16_t i = 0; i < strip.numPixels(); i++) {
        strip.setPixelColor(i, strip.Color(red, green, blue));
      }
      strip.show();
    }
  }
  if (mode == "on"){
    if (animate == 8){
      peperHot(animate_wait);
    }
  }
  if (mode == "on"){
    if (animate == 9){
      peperFlash();
    }
  }
  if (mode == "on"){
    if (animate == 10){
      peperFlash();
    }
  }
  if (mode == "on"){
    if (animate == 11){
      nightRider(strip.Color(255, 0, 0));
    }
  }
  if (mode == "on"){
    if (animate == 13){
      fadeTest();
    }
  }
}

void rainbowCycle(uint8_t wait) {
  // Generic Animation
  // Animation ID 1
  uint16_t i, j;
  for(j=0; j<256*5; j++) { // 5 cycles of all colors on wheel
    for(i=0; i< strip.numPixels(); i++) {
      server.handleClient();
      if (mode == "off"){
        break;
      }
      strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
    }
    if (mode == "off"){
        break;
      }
    strip.show();
    delay(wait); // @todo: make this a static var probably
  }
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g  b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}

static void chase(uint32_t c) {
  // Generic Animation
  // Animation ID 2, 3 4
  for(uint16_t i=0; i<strip.numPixels()+8; i++) {
      strip.setPixelColor(i  , c); // Draw new pixel
      strip.setPixelColor(i-8, 0); // Erase pixel a few steps back
      strip.show();
      delay(animate_wait);
      server.handleClient();
      if (mode == "off"){
        break;
      }
  }
}

static void police(uint32_t wait) {
  // Speciifc to the Robot Top Hat
  // Animastion ID 5
  server.handleClient();
  for(uint16_t i=0; i < 40; i++) {
    strip.setPixelColor(i, strip.Color(0, 0, 255));
  }
  for(uint16_t i=68; i < 108; i++) {
    strip.setPixelColor(i, strip.Color(255, 0, 0));
  }
  strip.show();
  delay(wait);
  server.handleClient();
  for(uint16_t i=0; i < 40; i++) {
    strip.setPixelColor(i, strip.Color(255, 0, 0));
  }
  for(uint16_t i=68; i < 108; i++) {
    strip.setPixelColor(i, strip.Color(0, 0, 255));
  }
  strip.show();
  delay(wait);
}

static void police2(uint32_t wait) {
  // Speciifc to the Robot Top Hat
  // Animastion ID 6
  for(uint16_t i=0; i < 40; i++) {
    strip.setPixelColor(i, strip.Color(255, 0, 0));
  }
  for(uint16_t i=41; i < 68; i++) {
    strip.setPixelColor(i, strip.Color(255, 255, 255));
  }
  for(uint16_t i=68; i < 108; i++) {
    strip.setPixelColor(i, strip.Color(0, 0, 255));
  }
  for(uint16_t i=108; i < 136; i++) {
    strip.setPixelColor(i, strip.Color(0, 0, 0));
  }

  strip.show();
  delay(wait);
  server.handleClient();
  for(uint16_t i=0; i < 40; i++) {
    strip.setPixelColor(i, strip.Color(0, 0, 255));
  }
  for(uint16_t i=41; i < 68; i++) {
    strip.setPixelColor(i, strip.Color(0, 0, 0));
  }
  for(uint16_t i=68; i < 108; i++) {
    strip.setPixelColor(i, strip.Color(255, 0, 0));
  }
  for(uint16_t i=108; i < 136; i++) {
    strip.setPixelColor(i, strip.Color(255, 255, 255));
  }
  strip.show(); 
  delay(wait);
}

void peperHot(uint8_t wait) {
  // Animate 8
  // ** NEW UNSTESTED **
  uint16_t i, b;
  for(i=0; i< strip.numPixels(); i++){
    server.handleClient();
    if (mode == "off"){
      break;
    }
    strip.setPixelColor(i, strip.Color(0, 0, 0));
  }
  strip.show();
  for(b=0; b < 256; b++){
    for(i=0; i< strip.numPixels(); i++) {
      server.handleClient();
      if(mode == "off"){
        break;
      }
      strip.setPixelColor(i, strip.Color(b, 0, 0));
    }
    strip.show();
    delay(wait);
  }
  for(b=255; b > 0; b =b - 1){
    for(i=0; i< strip.numPixels(); i++) {
      server.handleClient();
      if(mode == "off"){
        break;
      }
      strip.setPixelColor(i, strip.Color(b, 0, 0));
    }
    strip.show();
    delay(wait);
  }
}

void peperFlash() {
  // Animate 9
  // ** NEW UNSTESTED **
  uint16_t i;
  for(i=0; i< strip.numPixels(); i++) {
    server.handleClient();
    if (mode == "off"){
      break;
    }
    strip.setPixelColor(i, 0);
  }
  strip.show();
  delay(5);
  for(i=0; i< strip.numPixels(); i++) {
    server.handleClient();
    if (mode == "off"){
      break;
    }
    strip.setPixelColor(i, strip.Color(255, 255, 255));
  }
  strip.show();
  delay(5);
}

static void nightRider(uint32_t c) {
  // Animate 11
  // ** NEW UNSTESTED **
  uint16_t i, b, x;
  strip.setPixelColor(i, strip.Color(255, 0, 0));
  for(uint16_t i=0; i < strip.numPixels() / 2; i++) {
      b = (strip.numPixels() / 2) + i;
      x = ((strip.numPixels() / 2) + 1) - i;
      strip.setPixelColor(b, c); // Draw new pixel
      strip.setPixelColor(x, c);
      strip.setPixelColor(b - 4, 0); // Erase pixel a few steps back
      strip.setPixelColor(x - 4, 0);
      strip.show();
      delay(10);
      server.handleClient();
      if (mode == "off"){
        break;
      }
  }
  for(uint16_t i=0; i < strip.numPixels() / 2; i++) {
      b = 0 + i;
      x = strip.numPixels() - i;
      strip.setPixelColor(b, c); // Draw new pixel
      strip.setPixelColor(x, c);
      strip.setPixelColor(b - 4, 0); // Erase pixel a few steps back
      strip.setPixelColor(x - 4, 0);
      strip.show();
      delay(10);
      server.handleClient();
      if (mode == "off"){
        break;
      }
  }
}

static void fadeTest(){
  // Animate 13
  // ** NEW UNSTESTED **
  int R = 0;
  int G = 0;
  int B = 0;
  int i = 0;
  int j = 0;
  for(R && G && B; R < 126 && G < 126 && B; R++ && G++ && B++){
    for(int i=0; i< strip.numPixels(); i++){
      strip.setPixelColor(i, strip.Color(R, G, B));
      strip.show();
      delay(0);
    }
    server.handleClient();
    if (mode == "off"){
      break;
    }
    delay(1);
  }
  for(R && G && B; R >-1 && G >-1 && B >-1; R-- && G-- && B--){
    for(j=0; j < strip.numPixels(); j++){
      strip.setPixelColor(j, strip.Color(R, G, B));
      strip.show();
      delay(0);
    }
    server.handleClient();
    if (mode == "off"){
      break;
    }
    delay(1);
  }
}

static void boot(){
  // ** NEW UNSTESTED **
  uint32_t color = strip.Color(0, 0, 0);
  int i = 0;
  int j = 0;
  int rounds = 0;
  for(rounds = 0; rounds < 10; rounds++){
    for(i = 0; i < 150; i++){
      color = strip.Color(i, i, i);
      for(j = 0; j < strip.numPixels(); j++){
        strip.setPixelColor(j, color);
      }
      strip.show();
      server.handleClient();
      if (mode == "off"){
        break;
      }
      delay(10);
    }
    delay(100);
    for(i = 150; i > 150; i--){
      color = strip.Color(i, i, i);
      for(j = strip.numPixels(); j > strip.numPixels(); j--){
        strip.setPixelColor(j, color);
      }
      strip.show();
      server.handleClient();
      if (mode == "off"){
        break;
      }
      delay(10);
    }
  }

}