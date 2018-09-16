#define RightDIR 13
#define RightPWM 12

#define LeftDIR 9
#define LeftPWM 10

void setup() {
pinMode(RightDIR,OUTPUT);
pinMode(RightPWM,OUTPUT);
pinMode(LeftDIR,OUTPUT);
pinMode(LeftPWM,OUTPUT);

digitalWrite(RightDIR,LOW);
digitalWrite(RightPWM,LOW);
digitalWrite(LeftDIR,LOW);
digitalWrite(LeftPWM,LOW);

}

void loop() { 
  digitalWrite(RightDIR,LOW);
  analogWrite(RightPWM, 127);
  digitalWrite(LeftDIR,LOW);
  analogWrite(LeftPWM, 127);
  delay(3000);
  digitalWrite(LeftPWM,LOW);
  digitalWrite(RightPWM,LOW); 
  delay(1000);
  digitalWrite(LeftDIR,HIGH);
  analogWrite(LeftPWM, 127);
  digitalWrite(RightDIR,HIGH);
  analogWrite(RightPWM, 127);
  delay(3000);
}
