
void setup() {
Serial.begin(9600);
pinMode(6,OUTPUT); // RED LED
pinMode(7,OUTPUT); // GREEN LED
pinMode(8,OUTPUT); // Output 4 active HIGH
pinMode(9,OUTPUT); // Output 3 active HIGH
pinMode(10,OUTPUT); // Output 2 active HIGH
pinMode(11,OUTPUT); // Output 1 active HIGH
pinMode(12,OUTPUT); // DUT POWER active HIGH
pinMode(13,OUTPUT); // CANTEST active HIGH
digitalWrite(6,HIGH); //RED LED ON
digitalWrite(7,HIGH); //GREEN LED ON
digitalWrite(8,LOW); //OUTPUT 4 OFF
digitalWrite(9,LOW); //OUTPUT 3 OFF
digitalWrite(10,LOW); //OUTPUT 2 OFF
digitalWrite(11,LOW); //OUTPUT 1 OFF
digitalWrite(12,LOW); //DUT POWER OFF
digitalWrite(13,LOW); //CANTEST OFF -> Route CAN trough
Serial.println("START");
}
void loop() {
if (Serial.available()) {                     //Read String from Serial
message = Serial.readString();
}
if (message.length() != 0) {                    // Check if message is empty
if (message.substring(0,4) == "ccan") {          //Perform CAN Test
Serial.println("OK");                         // ACK
digitalWrite(13,HIGH);                        //Switch K1
delay(100);                                   //Wait for K1
if (analogRead(A0) > 150) {                   //Read ADC1 - Values below 120 are OK. If value is above 120, termination is not set or connection is bad.
Serial.println("FAIL");                       // Test failed
digitalWrite(12,LOW);                        // Reset K2 - TPU and IO Power
digitalWrite(13,LOW);                         // Reset K1
}
else {
Serial.println("PASS");                       // Test passed
digitalWrite(13,LOW);                         // Reset K1
digitalWrite(12,HIGH);                        // Enable K2 - TPU and IO Power
}
}
if (message.substring(0,5) == "reset") {          //Reset command
Serial.println("OK");                         // ACK
digitalWrite(6,HIGH); //RED LED ON
digitalWrite(7,HIGH); //GREEN LED ON
digitalWrite(8,LOW); //OUTPUT 4 OFF
digitalWrite(9,LOW); //OUTPUT 3 OFF
digitalWrite(10,LOW); //OUTPUT 2 OFF
digitalWrite(11,LOW); //OUTPUT 1 OFF
digitalWrite(12,LOW); //DUT POWER OFF
digitalWrite(13,LOW); //CANTEST OFF -> Route CAN trough
Serial.println("START");
}
if (message.substring(0,2) == "so") {          //Set Output command
Serial.println("OK");                         // ACK
if (message.substring(2,3) == "1") {           // Set Output1
  digitalWrite(11,HIGH);
  Serial.println("Output 1 "+message.substring(2,3));
}
else {
  digitalWrite(11,LOW);
  Serial.println("Output 1 "+message.substring(2,3));
}
if (message.substring(3,4) == "1") {           // Set Output2
  digitalWrite(10,HIGH);
   Serial.println("Output 2 "+message.substring(3,4));
}
else {
  digitalWrite(10,LOW);
  Serial.println("Output 2 "+message.substring(3,4));
}
if (message.substring(4,5) == "1") {           // Set Output3
  digitalWrite(9,HIGH);
   Serial.println("Output 3 "+message.substring(4,5));
}
else {
  digitalWrite(9,LOW);
  Serial.println("Output 3 "+message.substring(4,5));
}
if (message.substring(5,6) == "1") {           // Set Output4
  digitalWrite(8,HIGH);
   Serial.println("Output 4 "+message.substring(5,6));
}
else {
  digitalWrite(8,LOW);
  Serial.println("Output 4 "+message.substring(5,6));
}
}
if (message.substring(0,2) == "ri") {          //Read input command
Serial.println("OK");                         // ACK
delay(10);
bool one = false;
bool two = false;
bool three = false;
bool four = false;
if (analogRead(A1) > 800) {
one = true;
}
if (analogRead(A2) > 800) {
two = true;
}
if (analogRead(A3) > 800) {
three = true;
}
if (analogRead(A4) > 800) {
four = true;
}
Serial.println("ri"+String(!one)+String(!two)+String(!three)+String(!four));     //Read Input, invert and output
}
message = "";                                   //clear message string
}
}