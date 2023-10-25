// #pragma once

//    >>>>>>>>>>>  Update 05/07/66 Time = 16:04  <<<<<<<<<<<<
// Ethernet
#include <Arduino.h>
#include <Ethernet.h>
#include <EthernetServer.h>
// MQTT
#include <SPI.h>
#include <HardwareSerial.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
// Modbus Master 
#include <ModbusMaster.h>

#define LED_LAN PB8 // Note High state = LED on  >>> RX
#define LED_DATA PB9 // Note High state = LED on >>> TX

//  USART3
#define MAX485_DE_RE PB12
#define slaveID     1

#define NRST_PIN 7

#define D0_PIN PA3  
#define D1_PIN PA2
#define WIEGAND_DELAY_MICROSECONDS 20

const int WIEGAND_TOTAL_BITS = 35;
const int WIEGAND_OFFSET_BITS = 14;
const int WIEGAND_RANGE_BITS = 20;
const int WIEGAND_DELAY_US = 50;
const int adjustedValue = 170;

String OFFSET_VALUE = "00000000000000";

int recieved_data;

int x ;

int bit_data[35];

// Enter a MAC address and IP address for your controller below.
byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};

IPAddress ip(192, 168, 1, 250);       // The IP address STM32
IPAddress myDns(192, 168, 1, 1);      // The IP address วง LAN
IPAddress gateway(192, 168, 1, 1);    //
IPAddress subnet(255, 255, 255, 0);   // Subnet Mark

// กำหนดค่า MQTT broker
const char* mqttServer = "192.168.1.100";   // IP Local MQTT host
const int mqttPort = 1883;         
const char* mqttUsername = "1234";
const char* mqttPassword = "1234";
const char* mqttTopic = "topic/MPPT"; // กำหนด topic สำหรับการส่ง MQTT


EthernetClient ethClient;             // have
PubSubClient mqttClient(ethClient);   // have


void Ethernet_chenk();
void sendWiegand(int numberValue);


int temp ;   //  Sample test



EthernetServer server(3333);

String recieved_number = "";
int client_id;

// Json form to MQTT

StaticJsonDocument<200> jsonDoc_PV;
StaticJsonDocument<200> jsonDoc_Load;
StaticJsonDocument<200> jsonDoc_Batt;
StaticJsonDocument<200> jsonDoc_Over;

int Modbus_Error ;

//>>>>>>>>>>>>>>>>>>>>>>>>>>>>   Set UP   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

float PV_Voltage;
float PV_Current;
float PV_Power;
float Batt_Voltage;
float Batt_Current;
float Batt_Power;
float Load_Voltage;
float Load_Current;
float Load_Power;
float Batt_Temp;
float Batt_SOC;

float Co2_Reduction;
float Solar_Product;
float Consum_Energy;
float Total_Product;
float Total_Consum;
//float Total_Consum1;

//int Total_Solution;

ModbusMaster node;

void setup() 
{
  //  Reset NSRT Button 

   pinMode(NRST_PIN, OUTPUT);


  // >>>>  Modbus register RS-485   <<<<<<<<<

  Serial.begin(250000);
  Serial.println("Hello STM32");

  Serial2.begin(115200);
  Serial.println("Hello RS-485");

  pinMode(LED_LAN,  OUTPUT);
  pinMode(LED_DATA, OUTPUT);
  pinMode(D0_PIN, OUTPUT);
  pinMode(D1_PIN, OUTPUT);
  digitalWrite(LED_LAN, LOW);
  digitalWrite(LED_DATA, LOW);
 
 // RS-485
  pinMode(MAX485_DE_RE, OUTPUT);
  node.begin(slaveID, Serial2);

  // Callbacks allow us to configure the RS485 transceiver correctly
  node.preTransmission(preTransmission);
  node.postTransmission(postTransmission);


  Ethernet.init(PA4); // Ethernet CS pin

  //-------------------- Connect to Ethernet --------------------//
  
  Ethernet.begin(mac, ip);  // have
  // Ethernet_chenk();

  //------------------ End Connect to Ethernet ------------------//
  
  // <<<<<<<<<<<  MQTT start connecting Server
  mqttClient.setServer(mqttServer, mqttPort); // กำหนดที่อยู่ IP และพอร์ตของ MQTT broker
  mqttClient.setCallback(callback); // กำหนดฟังก์ชัน callback สำหรับการรับข้อมูลจาก MQTT broker
  connectToMQTT();

}

void loop() 
{
 
 Ethernet_chenk();

 


 // --------------------------------------------   End     RS-485



  // >>>>>>>>>>>>>>>>>>  MQTT >>>>>>>>>>>>>>>>>>>>>>>>>

 if (!mqttClient.connected() ) {
    
    mqttClient.setServer(mqttServer, mqttPort);
// test 

  pinMode(LED_LAN,  OUTPUT);
  pinMode(LED_DATA, OUTPUT);
  pinMode(D0_PIN, OUTPUT);
  pinMode(D1_PIN, OUTPUT);
  digitalWrite(LED_LAN, LOW);
  digitalWrite(LED_DATA, LOW);
 
 

  


  Ethernet.init(PA4); // Ethernet CS pin

  //-------------------- Connect to Ethernet --------------------//
  
  Ethernet.begin(mac, ip);  // have
  // Ethernet_chenk();

  //------------------ End Connect to Ethernet ------------------//



// test End
   
  digitalWrite(NRST_PIN, HIGH); // ตั้งค่า NRST_PIN เป็นสถานะ HIGH (1)
  delay(1000); // รอเป็นเวลา 1 วินาที
  
  digitalWrite(NRST_PIN, LOW); // ตั้งค่า NRST_PIN เป็นสถานะ LOW (0)
  delay(1000); // รอเป็นเวลา 1 วินาที

    
    //connectToMQTT();
    reconnectToMQTT();
  }

  mqttClient.loop();

  // ตัวอย่างการส่งข้อมูลผ่าน MQTT
  if (mqttClient.connected()) {
    mqttClient.publish("topic/publish", "Hello, MQTT!");
   // delay(5000);
  
  Serial.print("\n\n ...   Sending MQTT Message --> ");
  Serial.print(mqttClient.connected());
  Serial.print("< True >\n\n");
  }

  // temp = random(30,35);
  


  mqttClient.publish("topic/publish", "Working");
  mqttClient.publish("topic/Send temp", " Runing... ");

  // >>>>>>>>>>>>>>>>>   Test send with Json

  // ตัวอย่างการสร้างและส่งข้อมูล JSON ผ่าน MQTT
  if (mqttClient.connected()) {
 //   สร้าง JSON object
    jsonDoc_PV["PV_Voltage"] = PV_Voltage;

    jsonDoc_PV["PV_Current"] = PV_Current;

    jsonDoc_PV["PV_Power"] = PV_Power;
    
    jsonDoc_PV["Modbus_Read"] = Modbus_Error ;



    jsonDoc_Load["Load_Voltage"] = Load_Voltage;

    jsonDoc_Load["Load_Current"] = Load_Current;

    jsonDoc_Load["Load_Power"] = Load_Power;



    jsonDoc_Batt["Batt_Voltage"] = Batt_Voltage;

    jsonDoc_Batt["Batt_Current"] = Batt_Current;

    jsonDoc_Batt["Batt_Power"] = Batt_Power;

    jsonDoc_Batt["Batt_Temp"] = Batt_Temp;

    jsonDoc_Batt["Batt_SOC"] = Batt_SOC;   

    

    jsonDoc_Over["Co2_Reduction"] = Co2_Reduction;

    jsonDoc_Over["Solar_Product"] = Solar_Product;

    jsonDoc_Over["Consum_Energy"] = Consum_Energy;

    jsonDoc_Over["Total_Product"] = Total_Product;

    jsonDoc_Over["Total_Consum"] = Total_Consum;
  

    // แปลง JSON object เป็น string
    String jsonString_PV;
    String jsonString_Load;
    String jsonString_Batt;
    String jsonString_Over;

    serializeJson(jsonDoc_PV, jsonString_PV);
    serializeJson(jsonDoc_Load, jsonString_Load);
    serializeJson(jsonDoc_Batt, jsonString_Batt);
    serializeJson(jsonDoc_Over, jsonString_Over);

  

    // ส่งข้อมูลผ่าน MQTT
    mqttClient.publish("Solar/MPPT_PV", jsonString_PV.c_str());
    mqttClient.publish("Solar/MPPT_Load", jsonString_Load.c_str());
    mqttClient.publish("Solar/MPPT_Batt", jsonString_Batt.c_str()); 
    mqttClient.publish("Solar/MPPT_Over", jsonString_Over.c_str());

    delay(5000);
  }

  
 if(mqttClient.connected()){
       x = 99 ;
      digitalWrite(LED_LAN, HIGH);
      delay(100);
      digitalWrite(LED_LAN, LOW);
      delay(100);
 }

Read_RS_485();


}   //  End of Loop


// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  Void >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


void Ethernet_chenk()
{
  // Check for Ethernet hardware present
  if (Ethernet.hardwareStatus() == EthernetNoHardware) 
  {
    
    Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
    while (true) 
    {
      digitalWrite(LED_LAN, HIGH);
      delay(100);
      digitalWrite(LED_LAN, LOW);
      delay(100);
      // delay(1); // do nothing, no point running without Ethernet hardware
    }
  }

  if (Ethernet.linkStatus() == LinkOFF) 
  {
    Serial.println("Ethernet cable is not connected.");
    for(int i=0; i<5; i++)
    {
      digitalWrite(LED_LAN, HIGH);
      delay(50);
      digitalWrite(LED_LAN, LOW);
      delay(300);
    }
  }
  digitalWrite(LED_LAN, HIGH);

  //Serial.println(Ethernet.localIP());
  server.begin();
}

// ------------------------------------------------------------------->   connect MQTT

void connectToMQTT() {
  while (!mqttClient.connected()) {

    mqttClient.setServer(mqttServer, mqttPort); // กำหนดที่อยู่ IP และพอร์ตของ MQTT broker
    Serial.println("Connecting to MQTT...");
    
    mqttClient.connect("STM32Client", mqttUsername, mqttPassword);
  
    delay(1000);

    if(mqttClient.connected()){

      Serial.println("Connected to MQTT! >>> Success ");
      mqttClient.subscribe("topic/subscribe"); // ตัวอย่างการ subscribe topic
    } 
    else
    {
      Serial.print("Failed to connect :(  , retrying in 5 seconds...");
      delay(5000);
    }
  }
}

// ------------------------------------------------------------------->  Reconnect  connect MQTT


void reconnectToMQTT() {
  while (!mqttClient.connected()) {
  
  digitalWrite(NRST_PIN, HIGH); // ตั้งค่า NRST_PIN เป็นสถานะ HIGH (1)
  delay(1000); // รอเป็นเวลา 1 วินาที
  
  digitalWrite(NRST_PIN, LOW); // ตั้งค่า NRST_PIN เป็นสถานะ LOW (0)
  delay(1000); // รอเป็นเวลา 1 วินาที
    
    
  mqttClient.loop();
  

    mqttClient.setServer(mqttServer, mqttPort); // กำหนดที่อยู่ IP และพอร์ตของ MQTT broker
    // mqttClient.connect("STM32Client", mqttUsername, mqttPassword);
  
    Serial.println("Reconnecting to MQTT... Ver 2 ...");

    if (mqttClient.connect("STM32Client", mqttUsername, mqttPassword)) {
      Serial.println("Connected to MQTT!");
      mqttClient.subscribe("topic/subscribe"); // ตัวอย่างการ subscribe topic   
    } 
    
    else {
      Serial.println("Failed to reconnect to MQTT, retrying in 5 seconds... Loop reconnect   State Clien is -->>> ");
      //Serial.print(lient.state());
      delay(500);
    }
  }
}

// ------------------------------------------------------------------->   Callback 

void callback(char* topic, byte* payload, unsigned int length) {
  // ตัวอย่างการรับข้อมูลจาก MQTT broker
  Serial.print("Message received in topic: ");
  Serial.println(topic);
  Serial.print("Payload: ");
}

//     -------------------------------------------------- ----------->>>>>>>>>  RS-485

void preTransmission()
{
  digitalWrite(MAX485_DE_RE, HIGH);
}

void postTransmission()
{
  digitalWrite(MAX485_DE_RE, LOW);
}





// ------------------------------------------------------------------->>>>>>>>>>>>>   Read RS-485





void Read_RS_485()
{
   int result = node.readInputRegisters(12544, 3);
  if(result == node.ku8MBSuccess)
  {
    PV_Voltage = node.getResponseBuffer(0)/100.0f;
    PV_Current = node.getResponseBuffer(1)/100.0f;
    PV_Power = node.getResponseBuffer(2)/100.0f;

    Serial.print("\n\nPV Voltage : ");
    Serial.print(PV_Voltage);
    Serial.println(" Voltage.");
    Serial.print("PV Current : ");
    Serial.print(PV_Current);
    Serial.println(" Ampere.");
    Serial.print("PV Power : ");
    Serial.print(PV_Power);
    Serial.println(" Watt.");
    Serial.print("Status Modbud_Read : ");
    Serial.println(Modbus_Error);
  }

  int result2 = node.readInputRegisters(12548, 3);
  if(result2 == node.ku8MBSuccess)
  {
    Batt_Voltage = node.getResponseBuffer(0)/100.0f;
    Batt_Current = node.getResponseBuffer(1)/100.0f;
    Batt_Power = node.getResponseBuffer(2)/100.0f;

    Serial.print("Battery Voltage : ");
    Serial.print(Batt_Voltage);
    Serial.println(" Voltage.");
    Serial.print("Battery Current : ");
    Serial.print(Batt_Current);
    Serial.println(" Ampere.");
    Serial.print("Battery Power : ");
    Serial.print(Batt_Power);
    Serial.println(" Watt.");
  }

  int result3 = node.readInputRegisters(12556, 3);
  if(result3 == node.ku8MBSuccess)
  {
    Load_Voltage = node.getResponseBuffer(0)/100.0000f;
    Load_Current = node.getResponseBuffer(1)/100.0000f;
    Load_Power = node.getResponseBuffer(2)/100.0000f;

    Serial.print("Load Voltage : ");
    Serial.print(Load_Voltage);
    Serial.println(" Voltage.");
    Serial.print("Load Current : ");
    Serial.print(Load_Current);
    Serial.println(" Ampere.");
    Serial.print("Load Power : ");
    Serial.print(Load_Power);
    Serial.println(" Watt.");
  }

  int result4 = node.readInputRegisters(13085, 1);
  if(result4 == node.ku8MBSuccess)
  {
    Batt_Temp = node.getResponseBuffer(0)/100.0f;

    Serial.print("Batt Temp : ");
    Serial.print(Batt_Temp);
    Serial.println(" °C.");
  }

  int result5 = node.readInputRegisters(12570, 1);
  if(result5 == node.ku8MBSuccess)
  {
    Batt_SOC = node.getResponseBuffer(0)/1.0f;

    Serial.print("Batt SOC : ");
    Serial.print(Batt_SOC);
    Serial.println(" %");
  }

  int result6 = node.readInputRegisters(13076, 1);
  if(result6 == node.ku8MBSuccess)
  {
    Co2_Reduction = node.getResponseBuffer(0)*1000000/100.0f;

    Serial.print("Co2 Reduction : ");
    Serial.print(Co2_Reduction);
    Serial.println(" Kg CO2 eq.");
  }

  int result7 = node.readInputRegisters(13068, 2);
  if(result7 == node.ku8MBSuccess)
  {
    int Solar_ProductLow = node.getResponseBuffer(0);
    int Solar_ProductHigh = node.getResponseBuffer(1);
    int Solar_Int = Modbus_HL(Solar_ProductLow, Solar_ProductHigh);
    Solar_Product = (Solar_Int*1000)/100.0f;
    Serial.print("Solar Product : ");
    Serial.print(Solar_Product);
    Serial.println(" Wh.");
  }

  int result8 = node.readInputRegisters(13060, 2);
  if(result8 == node.ku8MBSuccess)
  {
    int Consum_EnergyLow = node.getResponseBuffer(0);
    int Consum_EnergyHigh = node.getResponseBuffer(1);
    int Consum_Energy_Int = Modbus_HL(Consum_EnergyLow, Consum_EnergyHigh);
    Consum_Energy = (Consum_Energy_Int*1000)/100.0f;

    Serial.print("Consum Energy : ");
    Serial.print(Consum_Energy);
    Serial.println(" Wh.");
  }

  int result9 = node.readInputRegisters(13074, 2);
  if(result9 == node.ku8MBSuccess)
  {
    int Total_ProductLow = node.getResponseBuffer(0);
    int Total_ProductHigh = node.getResponseBuffer(1);
    int Total_Product_Int = Modbus_HL(Total_ProductLow, Total_ProductHigh);
    Total_Product = (Total_Product_Int*1000)/100.0f;

    Serial.print("Total Product : ");
    Serial.print(Total_Product);
    Serial.println(" Wh.");
  }

  int result10 = node.readInputRegisters(13066, 1);
  if(result10 == node.ku8MBSuccess)
  {
    int Total_ConsumLow = node.getResponseBuffer(0);
    int Total_ConsumHigh = node.getResponseBuffer(1);
    int Total_Consum_Int = Modbus_HL(Total_ConsumLow, Total_ConsumHigh);
    Total_Consum = (Total_Consum_Int*1000)/100.0f;

    Serial.print("Total Consum : ");
    Serial.print(Total_Consum);
    Serial.println(" Wh.");
    Modbus_Error = 1 ;
  }

   

  else
  {
    Serial.print("Modbus Error:  ");
    Modbus_Error = 0;
    Serial.println(result, HEX);

  }


}


      // Convert High + Low from modbusRegister
      
    int Modbus_HL(int LowValue, int HighValue) {
      int High_Value = HighValue;
      int Low_Value = LowValue;

      // แปลง A เป็น hex
      String hexA = intToHex(High_Value);

      // แปลง B เป็น hex
      String hexB = intToHex(Low_Value);

      // นำ hex A และ hex B มาต่อกันเป็น string
      String concatenatedString = hexA + hexB;
      //Serial.println(concatenatedString);
      // Serial.print("hexA --> ");
      // Serial.println(hexA); // พิมพ์ผลลัพธ์ทาง Serial Monitor
      // Serial.print("haxB --> ");
      // Serial.println(hexB); // พิมพ์ผลลัพธ์ทาง Serial Monitor
      

      // แปลง string เป็น int
      int C = hexToInt(concatenatedString);
      // Serial.print(" C --> ");
      //Serial.println(C); // พิมพ์ผลลัพธ์ทาง Serial Monitor
      delay(1000); // หน่วงเวลา 1 วินาที
      return C;
    }

    String intToHex(int value) {
      String hexString = String(value, HEX); // แปลงเลขฐานสิบเป็น hex
      return hexString;
    }

    int hexToInt(String hexString) {
      char charArray[hexString.length() + 1];
      hexString.toCharArray(charArray, hexString.length() + 1);

      int intValue = (int)strtol(charArray, NULL, 16); // แปลง string hex เป็น int
      return intValue;
    }








