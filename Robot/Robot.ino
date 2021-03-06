#include <EEPROM.h>
#include "PacketSerial.h"
#define BOT_ID 1
#define STARTBYTE 0xFF
#define PACKETSIZE 254
#define MINPACKET 8
#define TCP 1
#define ADHOC 0
#define FWD 0
#define ACK 1
#define ADDRESS 0

#define MOTOR_LEFT_PWM  10
#define MOTOR_LEFT_DIR  9
#define MOTOR_RIGHT_PWM 12
#define MOTOR_RIGHT_DIR  13

#define ULTRASONIC_FRONT_TRIGGER   43
#define ULTRASONIC_FRONT_ECHO   41

#define REDLED A11
#define WHITELED 44
#define YELLOWLED A12
#define ORANGELED 42


#define TIMER1COUNT 64286  //50Hz

//External commands, communicated with another robot (in Adhoc mode) or TCP
#define NOCOMMAND 0
#define MOVEFORWARD 0x01
#define MOVEFORWARDTIME 0x02
#define MOVEBACK 0x03
#define MOVEBACKTIME 0x04
#define TURNLEFT 0x05
#define TURNRIGHT 0x06
#define STOP 0x07
#define DISTANCEFRONT 0x0A
#define GETHEADING 0x0D 
#define GETID 0x0F
#define RXDISTANCE 0x12 // Sury : Command to handle received distance


//Internal commands, communicated with ESP32
#define INT_ID 0x01
#define INT_SSID_PWD 0x02
#define INT_MATRIX 0x03
#define INT_RSSI 0x04
#define INT_IP 0x05
#define INT_DEMO 0x06

#define NODECOUNT 16

//Matrix - Robot ID 0 to ID 15
uint8_t matrix[NODECOUNT][NODECOUNT]={{1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
                                      {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
                                      {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
                                      {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
                                      {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
                                      {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
                                      {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
                                      {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
                                      {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
                                      {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
                                      {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
                                      {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
                                      {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
                                      {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
                                      {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
                                      {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1}};
char ssid[] = "AdHocRobots";
char password[] = "iliketomoveit";
char ip[] = {10,0,0,5};

uint8_t Command = 0;
long Rssi = 0;
unsigned long distance = 0;

uint8_t nodeID = 0;
uint8_t movementTime = 0;
uint16_t tempMovementTime = 0;

uint8_t rxDistance = 0; //<---------------------------------------------------- DISTANCE OF OTHER CAR
uint8_t MyDistance = 0; //<----------------------------------------------------- DISTANCE OF *THIS* CAR

uint16_t PacketCounter = 0;
long RSSI_Value = 0;

PacketSerial packetSerial;

uint8_t data[2];

//Handle commands. USER CAN ADD MODE COMMANDS IF NECESSARY
void handleCommands(uint8_t src, uint8_t dst, uint8_t internal, uint8_t tcp, uint8_t fwd, uint8_t counterH, uint8_t counterL, uint8_t datalen, uint8_t command, uint8_t *data)
{

    uint8_t tempData[32] = {0};
    data = data + 1;
    switch(command)
    {
      case MOVEFORWARD : Command = MOVEFORWARD;
                         moveForward();
                         break;

      case MOVEFORWARDTIME: moveForwardForTime(*data);
                            break;

      case MOVEBACK: Command = MOVEBACK; 
                     moveBack();
                     break;
                     
      case MOVEBACKTIME: moveBackForTime(*data);
                         break;
                         
      case STOP: Command = STOP; 
                 stopMotors();
                 break;
                
      case TURNLEFT: turnLeft(*data);
                     break;

      case TURNRIGHT: turnRight(*data);
                      break;

      case DISTANCEFRONT: distance = getDistanceFront();
                          if(distance > 254)
                          {
                           distance = 254;
                          }
                          tempData[0] = command;
                          tempData[1] = distance & 0xFF;
                          tempData[2] = 0;
                          sendPacket(dst, src, internal, tcp, ACK, counterH, counterL, 2, tempData);
                          break;

      case RXDISTANCE: checkDistance(*data);
                       break;
      
      case GETHEADING: break;   

      case GETID: nodeID = getID();
                  tempData[0] = command;
                  tempData[1] = nodeID;
                  sendPacket(dst, src, internal, tcp, ACK, counterH, counterL, 2, tempData);
                  break; 

    }

#define TCP 1
#define ADHOC 0
#define FWD 0
#define ACK 1
#define ADDRESS 0
  }

//Timer 1 interrupt service routine
ISR(TIMER1_OVF_vect)
{
 
 long time = millis();

 switch(Command)
 {

  case MOVEFORWARDTIME:
  case TURNLEFT:
  case TURNRIGHT:
  case MOVEBACKTIME:
  if(((uint16_t)(millis()/1000) - tempMovementTime) >= movementTime)
                      {
                        stopMotors();  
                        Command = NOCOMMAND; 
                      }
                     break;
 }

 TCNT1 = TIMER1COUNT;
}

void initGPIO()
{
 pinMode(MOTOR_RIGHT_PWM,OUTPUT);
 pinMode(MOTOR_RIGHT_DIR,OUTPUT);
 pinMode(MOTOR_LEFT_PWM,OUTPUT);
 pinMode(MOTOR_LEFT_DIR,OUTPUT);
 pinMode(REDLED,OUTPUT);
 pinMode(WHITELED,OUTPUT);
 pinMode(YELLOWLED,OUTPUT);
 pinMode(ORANGELED,OUTPUT);
 // DEBUG LED
 pinMode(53,OUTPUT); 
 stopMotors();

 pinMode(ULTRASONIC_FRONT_TRIGGER, OUTPUT);
 pinMode(ULTRASONIC_FRONT_ECHO, INPUT);
}


void initTimer()
{
  noInterrupts();   
  TCCR1A = 0;
  TCCR1B = 0;

  TCNT1 = TIMER1COUNT;
  TCCR1B |= (1 << CS12);
  TIMSK1 |= (1 << TOIE1);
  interrupts();
}

//Set LEDs
void setLED(uint8_t led, bool state)
{
  if(state)
  {
    digitalWrite(led,HIGH);
  }
  else
  {
    digitalWrite(led,LOW);
  }
  
}

//Get distance in cm from front ultrasonic sensor (In blocking mode)
uint8_t getDistanceFront()
{
 digitalWrite(ULTRASONIC_FRONT_TRIGGER, LOW); 
 delayMicroseconds(2); 

 digitalWrite(ULTRASONIC_FRONT_TRIGGER, HIGH);
 delayMicroseconds(10); 
 
 digitalWrite(ULTRASONIC_FRONT_TRIGGER, LOW);
 long duration = pulseIn(ULTRASONIC_FRONT_ECHO, HIGH);

 return duration/58.2;
}


void checkDistance(uint8_t data){
  
  rxDistance = data;
  //DEBUG
  Serial.println(rxDistance);
  while (rxDistance >= (MyDistance + 2)){
          moveForwardForTime(1); // MOVE 1 second and check MyDistance is Updated in MoveForwardForTime  
  }
  while (rxDistance <= (MyDistance - 2)){
          moveBackForTime(1); // MOVE 1 second and check MyDistance is Updated in MoveBackForTime
  }
}



  
// Move forward
void moveForward()
{
  stopMotors();
  
  digitalWrite(MOTOR_LEFT_DIR,LOW);
  digitalWrite(MOTOR_LEFT_PWM,HIGH);

  digitalWrite(MOTOR_RIGHT_DIR,LOW);
  digitalWrite(MOTOR_RIGHT_PWM,HIGH);

}

//Stop movement
void stopMotors()
{
  digitalWrite(MOTOR_LEFT_PWM,LOW);

  digitalWrite(MOTOR_RIGHT_PWM,LOW);

  delay(200);  
}

//Move forward for specific time (in seconds)
void moveForwardForTime(uint8_t data)
{
  moveForward();
  movementTime = data;
  tempMovementTime = (uint16_t)(millis()/1000);
  Command = MOVEFORWARDTIME;
  //MyDistance = ; <------------------------------------------- Find out how much the cars move in 1 second, 2 second, etc and write formula to update MyDistance here and in moveBackForTime
}

//Move back for specific time (in seconds)
void moveBackForTime(uint8_t data)
{
  moveBack();
  movementTime = data;
  tempMovementTime = (uint16_t)(millis()/1000);
  Command = MOVEBACKTIME;
  //MyDistance = ; <------------------------------------------- Find out how much the cars move in 1 second, 2 second, etc and write formula to update MyDistance here and in moveBackForTime
}

//Move back
void moveBack()
{
  stopMotors();
  digitalWrite(MOTOR_LEFT_DIR,HIGH);
  digitalWrite(MOTOR_LEFT_PWM,HIGH);

  digitalWrite(MOTOR_RIGHT_DIR,HIGH);
  digitalWrite(MOTOR_RIGHT_PWM,HIGH);
  
}

//Turn left for specific time (in seconds)
void turnLeft(uint8_t data)
{
  stopMotors();
  digitalWrite(MOTOR_RIGHT_DIR,LOW);
  digitalWrite(MOTOR_RIGHT_PWM,HIGH);
  
  movementTime = data;
  tempMovementTime = (uint16_t)(millis()/1000);
  Command = TURNLEFT;
}

//Turn right for specific time (in seconds)
void turnRight(uint8_t data)
{ 
  stopMotors();
  digitalWrite(MOTOR_LEFT_DIR,LOW);
  digitalWrite(MOTOR_LEFT_PWM,HIGH);

  movementTime = data;
  tempMovementTime = (uint16_t)(millis()/1000);
  Command = TURNRIGHT;
}

//Get RSSI from ESP32
void getRSSI()
{
  uint8_t data;
  sendPacket(nodeID, nodeID, INT_RSSI, TCP, FWD, 0, 0, 0, &data);
  //RSSI value is updated in RSS_Value variable as soon as there is reply from ESP32. This is implemented in OnPacket() function
}

//This is internal API used to enable demo mode in ESP32. Demo mode should be enabled in all the robots to make it work
void enableDemo()
{
  uint8_t data;
  sendPacket(nodeID, nodeID, INT_DEMO , TCP, FWD, 0, 0, 0, &data);
}

//Get ID of robot
uint8_t getID()
{
  return EEPROM.read(ADDRESS);
}

//Set ID of robot
void setID(uint8_t ID)
{
  EEPROM.write(ADDRESS, ID);
  delay(50);
  nodeID = getID();
}

//Send ID of robot to ESP32
void sendID()
{
  nodeID = getID();
  sendPacket(nodeID,nodeID,INT_ID,TCP,FWD,0,0,1,&nodeID);
}

//Send connection matrix to ESP32
void sendMatrix()
{
  nodeID = getID();
  sendPacket(nodeID,nodeID,INT_MATRIX,TCP,FWD,0,0,NODECOUNT,(uint8_t*)matrix[nodeID]);
}

//Send IP address of server to ESP32
void sendIP()
{
  sendPacket(nodeID,nodeID,INT_IP,TCP,FWD,0,0,sizeof(ip),ip);
}

//Send AP and password to ESP32
void sendSSIDandPassword()
{
  char *ssid_pwd = (char*)calloc(strlen(ssid)+strlen(password)+2,sizeof(char));
  strcpy(ssid_pwd,ssid);
  int delimiterLoc = strlen(ssid);
  ssid_pwd[delimiterLoc] = 0xA9;
  strcat(ssid_pwd,password);
  sendPacket(nodeID,nodeID,INT_SSID_PWD,TCP,FWD,0,0,strlen(ssid_pwd),ssid_pwd);
  free(ssid_pwd);
}

//This function is called when data is received from serial port (from PacketSerial library)
void onPacket(const uint8_t* buffer, size_t size)
{
  uint8_t src, dst, internal, tcp, fwd, counterH, counterL, datalen, command, *data;
  nodeID = getID();
  if((buffer[0] != STARTBYTE))
  {
    return;
  }
  if(size<7)
  {
    return;
  }
  src = buffer[1];
  dst = buffer[2];
  internal = (buffer[4] >> 5) & 0x07;
  tcp = (buffer[4] >> 4) & 0x01;
  fwd = (buffer[4] >> 3) & 0x01;
  counterH = buffer[5];
  counterL = buffer[6];
  datalen = buffer[7];
  command = buffer[8];
  data = (buffer + 8);

  // Checksum is not calculated. Can be implemented if necessary

  //Check if the command is internal, especially get RSSI from ESP32
  if(internal == INT_RSSI)
  {
    if(datalen != 5)
    {
      return;
    }
    //Update RSSI_Value variable with latest RSSI
    RSSI_Value = (long)(buffer[9] << 24) | (long)(buffer[10] << 16) | (long)(buffer[11] << 8) | (long)(buffer[12]);
    uint8_t temp[5];
    temp[0] = 0x08;
    temp[1] = RSSI_Value >> 24;
    temp[2] = RSSI_Value >> 16;
    temp[3] = RSSI_Value >> 8;
    temp[4] = RSSI_Value;
    //sendPacket(0, 0, 0, TCP, ACK, counterH, counterL, 5, temp);
  }
  else if(internal == INT_ID)
  {
    sendID();
  }
  else if(internal == INT_MATRIX)
  {
    sendMatrix();
  }
  else if(internal == INT_SSID_PWD)
  {
    sendSSIDandPassword();
  }
  else if(internal == INT_IP)
  {
    sendIP();
  }

  //Call callback function
  OnReceive(src, dst, internal, tcp, fwd, counterH, counterL, datalen, command, data);
}

//For internal use only
void sendPacket(uint8_t src, uint8_t dst, uint8_t internal, uint8_t isTCP, uint8_t isACK, uint8_t counterHigh, uint8_t counterLow, uint8_t dataLength, uint8_t *data)
{
 uint8_t packet[PACKETSIZE] = {0};
 int index = 0;
 uint8_t checksum = 0;
 nodeID = getID();
 
 packet[0] = STARTBYTE;
 packet[1] = src;
 packet[2] = dst;
 packet[3] = nodeID;
 packet[4] = (internal << 5) | (isTCP << 4) | (isACK << 3);
 packet[5] = counterHigh;
 packet[6] = counterLow;
 packet[7] = dataLength;
 for(index=0; index<dataLength; index++)
 {
  packet[8+index] = data[index];
 }
// packet[7+index] = checksum;  // Checksum is not calculated. Can be implemented if necessary
 packetSerial.send(packet,8+index);
}

//Initial setup
void setup() 
{
Serial.begin(115200);
setID(BOT_ID);
nodeID = getID();
packetSerial.setPacketHandler(&onPacket);
packetSerial.begin(115200);
initGPIO();
initTimer();
delay(2000);
sendID();
delay(1000);
sendMatrix();
delay(1000);
sendIP();
delay(1000);
sendSSIDandPassword();

//setLED(WHITELED,true);
//setLED(YELLOWLED,true);
//setLED(REDLED,true);
//setLED(ORANGELED,true); 

Serial.println("Arduino Serial test!");


}

bool once = true;
void loop() 
{
  packetSerial.update();
}
/** USER FUNCTION FOR AD-HOC NETWORKS COURSE. 
 function and send over WiFi network
src -> ID of robot. Send nodeID variable here (This is don't care for TCP packet)
dst -> ID of robot to which you want to send the packet (This is don't care for TCP packet)
isTCP -> Set with macro TCP or ADHOC depending where you want to send
dataLength -> Length of data
data -> Data that has to be sent. The first byte is COMMAND and subsequent bytes are arguments
**/
void CreatePacket(uint8_t src, uint8_t dst, uint8_t isTCP, uint8_t dataLength, uint8_t *data)
{
  PacketCounter++;
  uint8_t counterLow = PacketCounter & 0xFF;
  uint8_t counterHigh = (PacketCounter >> 8) & 0xFF;
  sendPacket(src, dst, 0x00, isTCP, FWD, counterHigh, counterLow, dataLength, data);
  
}

/** USER FUNCTION FOR AD-HOC NETWORKS COURSE. This function is called when a packet is received from TCP or AD-HOC node
//void onPacket(const uint8_t* buffer, size_t size) calls this function after parsing the packet.
**/
void OnReceive(uint8_t src, uint8_t dst, uint8_t internal, uint8_t tcp, uint8_t fwd, uint8_t counterH, uint8_t counterL, uint8_t datalen, uint8_t command, uint8_t *data)
{
      
  //Execute commands if the command is from TCP OR if ID is equal to destination (in Ad-hoc mode)
  if(tcp == TCP || ((tcp == ADHOC) && (nodeID == dst)))
  {       
    handleCommands(src, dst, internal, tcp, fwd, counterH, counterL, datalen, command, data);
    
    
    // JUR: TEST IF RECEIVED
    /*
    if (command == 0x12) {
      Serial.println("RECEIVED GET DISTANCE!");
    }
    */
    uint8_t dst_id = 3 - nodeID;            // hackish way to get destination ID, assuming only two bots used
    ForwardPacket(dst_id, command, data);
  }
  
}


/*
  JUR: Forward received packet to the second car
*/
void ForwardPacket(uint8_t dst, uint8_t command, uint8_t *data)
{
  uint8_t packet[3];
  packet[0] = command;
  packet[1] = data[1];
  packet[2] = data[0];

  //DEBUG
  /*
  Serial.println("Packet values Forwardpacket");
  Serial.println(packet[0]);
  Serial.println(packet[1]);
  Serial.println(packet[2]);
  */
  CreatePacket(BOT_ID, dst, 0, sizeof(packet), packet);
}
