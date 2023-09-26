import paho.mqtt.client as mqtt
import json

# MQTT Broker และพอร์ต (ให้แก้ไขตามการตั้งค่าของคุณ)
mqtt_broker = "localhost"  # MQTT Broker ของคุณ
mqtt_port = 1883  # พอร์ต MQTT

with open('DataFromCombineMod.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)

# # ข้อมูล JSON ที่คุณต้องการส่ง
# data_to_send = {
#     "sensor_id": "12345",
#     "temperature": 25.5,
#     "humidity": 50.0
# }

# Update_Master_Data
Update_Master_Data1 = json_object['Update_Master_Data']["cabinetList"]
Update_Master_Data2 = json_object['Update_Master_Data']
isCabinetActive1 = Update_Master_Data1[0]["isCabinetActive"]
isCabinetActive2 = Update_Master_Data1[1]["isCabinetActive"]
isCabinetActive3 = Update_Master_Data1[2]["isCabinetActive"]
cabinetCode1 = Update_Master_Data1[0]["cabinetCode"]
cabinetCode2 = Update_Master_Data1[1]["cabinetCode"]
cabinetCode3 = Update_Master_Data1[2]["cabinetCode"]
siteCode = Update_Master_Data2["siteCode"]
isSiteActive = Update_Master_Data2["isSiteActive"]
# Update_emergency_key
Update_emergency_key = json_object['Update_emergency_key']["cabinetList"]
emergencyKey1 = Update_emergency_key[0]['emergencyKey']
emergencyKey2 = Update_emergency_key[1]['emergencyKey']
isCabinetActive1 = Update_emergency_key[0]['isCabinetActive']
isCabinetActive2 = Update_emergency_key[1]['isCabinetActive']
deviceName = Update_emergency_key[0]['deviceName']
# Get_cabinet_status
Get_cabinet_status = json_object['Get_cabinet_status']["cabinets"]
site_code1 = Get_cabinet_status[0]['site_code']
site_code2 = Get_cabinet_status[1]['site_code']
cabinet_code1 = Get_cabinet_status[0]['cabinet_code']
cabinet_code2 = Get_cabinet_status[1]['cabinet_code']
locked1 = Get_cabinet_status[0]['locked']
locked2 = Get_cabinet_status[1]['locked']
is_emergency1 = Get_cabinet_status[0]['is_emergency']
is_emergency2 = Get_cabinet_status[1]['is_emergency']
last_updated1 = Get_cabinet_status[0]['last_updated']
last_updated2 = Get_cabinet_status[1]['last_updated']
emerg_key1 = Get_cabinet_status[0]['emerg_key']
emerg_key2 = Get_cabinet_status[1]['emerg_key']
mac_address1 = Get_cabinet_status[0]['mac_address']
mac_address2 = Get_cabinet_status[1]['mac_address']
device_name1 = Get_cabinet_status[0]['device_name']
device_name2 = Get_cabinet_status[1]['device_name']
# Lock_cabinet
Lock_cabinet = json_object['Lock_cabinet']
successL = Lock_cabinet['success']
messageL = Lock_cabinet['message']
# Unlock_cabinet
Unlock_cabinet = json_object['Unlock_cabinet']
successUL = Unlock_cabinet['success']
messageUL = Unlock_cabinet['message']
# Device_API
Device_API = json_object['Device_API']
successAPI = Device_API['success']
messageAPI = Device_API['message']
# Send_emergency_API
Send_emergency_API = json_object['Send_emergency_API']
emerg_keyAPI = Send_emergency_API['emerg_key']
# Device_alarm_on_off
Device_alarm_on_off = json_object['Device_alarm_on_off']
alarm_timer = Device_alarm_on_off['alarm_timer']
# json_Data_to_WD1
json_Data_to_WD1 = json_object['json_Data_to_WD1']
cabinet_serf = json_Data_to_WD1['cabinet_serf']
cabinet_sers = json_Data_to_WD1['cabinet_sers']
cabinet_serc = json_Data_to_WD1['cabinet_serc']
wacthdog_serf = json_Data_to_WD1['wacthdog_serf']
wacthdog_sers = json_Data_to_WD1['wacthdog_sers']
otp_serf = json_Data_to_WD1['otp_serf']
otp_sers = json_Data_to_WD1['otp_sers']
t_day = json_Data_to_WD1['t_day']
t_month = json_Data_to_WD1['t_month']
t_years = json_Data_to_WD1['t_years']
t_hour = json_Data_to_WD1['t_hour']
t_min = json_Data_to_WD1['t_min']
t_sec = json_Data_to_WD1['t_sec']



# run....
json_Data_to_WD1 = {
        "Data_mod" :[{
        "cabinet_serf" : cabinet_serf,
        "cabinet_sers" : cabinet_sers,
        "cabinet_serc" : cabinet_serc,
        "wacthdog_serf" : wacthdog_serf,
        "wacthdog_sers" : wacthdog_sers,
        "otp_serf" : otp_serf,
        "otp_sers" : otp_sers,
        "t_day" : t_day,
        "t_month" : t_month,
        "t_years" : t_years,
        "t_hour" : t_hour,
        "t_min" : t_min,
        "t_sec" : t_sec
        }]
}

Update_Master_Data = {
"cabinetList": [
    {
        "isCabinetActive": isCabinetActive1,
        "cabinetCode": cabinetCode1
    },
    {
        "isCabinetActive": isCabinetActive2,
        "cabinetCode": cabinetCode2
    },
    {
        "isCabinetActive": isCabinetActive3,
        "cabinetCode": cabinetCode3
    }
],
"siteCode": siteCode,
"isSiteActive": isSiteActive  #if cabinet A online or B online 
}

Update_emergency_key =  {
    "siteCode": siteCode,
    "cabinetList": [
        {
            "emergencyKey": emergencyKey1,
            "isCabinetActive": isCabinetActive1,
            "cabinetCode": cabinetCode1,
            "deviceName": deviceName
        },
        {
            "emergencyKey": emergencyKey2,
            "isCabinetActive": isCabinetActive2,
            "cabinetCode": cabinetCode2,
            "deviceName": deviceName
        }
    ],
    "isSiteActive": isSiteActive
}

Get_cabinet_status = {
    "cabinets" : [ 
        {
            "site_code" : site_code1,
            "cabinet_code" : cabinet_code1,
            "locked" : locked1,
            "is_emergency" : is_emergency1,
            "last_updated" : last_updated1,
            "emerg_key" : emerg_key1,
            "mac_address" : mac_address1,
            "device_name" : device_name1
            }, {

            "site_code" : site_code2,
            "cabinet_code" : cabinet_code2,
            "locked" : locked2,
            "is_emergency" : is_emergency2,
            "last_updated" : last_updated2,
            "emerg_key" : emerg_key2,
            "mac_address" : mac_address2,
            "device_name" : device_name2
        } 
    ]
}

Lock_cabinet = {
    "success" : successL,
    "message" : messageL
}

Unlock_cabinet = {
    "success" : successUL,
    "message" : messageUL
}

Device_API = {
    "success" : successAPI,
    "message" : messageAPI
}

Device_status_report_API = {
    "site_code": "100CP",
    "devices": [
        { 
            "serial": "", "cabinet_code": "100CP-1", "device_status_id": 1, "device_type_id": 1,
            "event_type_id": 2, "dt": "2019-07-16 17:29:00"},
        { 
            "serial": "", "cabinet_code": "100CP-1", "device_status_id": 1, "device_type_id": 2,
            "event_type_id": 5, "dt": "2019-07-16 17:29:00"},
        { 
            "serial": "", "cabinet_code": "100CP-1", "device_status_id": 1, "device_type_id": 10,
            "event_type_id": 11, "dt": "2019-07-16 17:29:00"},
        { 
            "serial": "", "cabinet_code": "100CP-1", "device_status_id": 1, "device_type_id": 7,
            "event_type_id": 6, "dt": "2019-07-16 17:29:00"},
        { 
            "serial": "", "cabinet_code": "E131M-2", "device_status_id": 0, "device_type_id": 6,
            "event_type_id": 0, "dt": "2019-07-16 17:29:00"},
        { 
            "serial": "", "cabinet_code": "E131M-2", "device_status_id": 1, "device_type_id": 1,
            "event_type_id": 0, "dt": "2019-07-16 17:29:00"},
        { 
            "serial": "", "cabinet_code": "E131M-2", "device_status_id": 0, "device_type_id": 10, 
            "event_type_id": 7, "dt": "2019-07-16 17:29:00"},
        { 
            "serial": "", "cabinet_code": "E131M-2", "device_status_id": 0, "device_type_id": 7,
            "event_type_id": 10, "dt": "2019-07-16 17:29:00"}
    ]
}

Send_emergency_API = {
    "emerg_key": emerg_keyAPI
}

# Device_send_image = {
#     "site_code": "",
#     "cabinet_code": "BKKYM-1",
#     "dt": "2019-03-27 12:00:11",
#     "img": "IMAGE_URL_GENERATE_BY_DEVICE"
# }

Device_alarm_on_off =  {
    "site_code": "",
    "cabinet_code": cabinet_code1,
    "alarm_timer": alarm_timer #Alarm time in second unit
}



# # รวมข้อมูลจากทั้งสองตัวแปร
# combined_data = {
#     "Update_Master_Data": Update_Master_Data,
#     "Update_emergency_key": Update_emergency_key,
#     "Get_cabinet_status": Get_cabinet_status,
#     "Lock_cabinet": Lock_cabinet,
#     "Unlock_cabinet": Unlock_cabinet,
#     "Device_API": Device_API,
#     "Device_status_report_API": Device_status_report_API,
#     "Send_emergency_API": Send_emergency_API,
#     "Device_send_image": Device_send_image,
#     "Device_alarm_on_off": Device_alarm_on_off,
#     "json_Data_to_WD1" : json_Data_to_WD1
# }



# ฟังก์ชันเมื่อเชื่อมต่อกับ MQTT Broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("เชื่อมต่อกับ MQTT Broker สำเร็จ")
        # ส่งข้อมูล JSON ที่นี่เมื่อเชื่อมต่อสำเร็จ
        client.publish("Update_Master_Data", json.dumps(Update_Master_Data))
        client.publish("Update_emergency_key", json.dumps(Update_emergency_key))
        client.publish("Get_cabinet_status", json.dumps(Get_cabinet_status))
        client.publish("Lock_cabinet", json.dumps(Lock_cabinet))
        client.publish("Unlock_cabinet", json.dumps(Unlock_cabinet))
        client.publish("Device_API", json.dumps(Device_API))
        client.publish("Device_status_report_API", json.dumps(Device_status_report_API))
        client.publish("Send_emergency_API", json.dumps(Send_emergency_API))
        # client.publish("Device_send_image", json.dumps(Device_send_image))
        client.publish("Device_alarm_on_off", json.dumps(Device_alarm_on_off))
        client.publish("json_Data_to_WD1", json.dumps(json_Data_to_WD1))
    
    else:
        print("เชื่อมต่อกับ MQTT Broker ไม่สำเร็จ, รหัสผลลัพธ์:", rc)

# สร้าง MQTT Client
client = mqtt.Client()

# กำหนดฟังก์ชันเมื่อเชื่อมต่อ
client.on_connect = on_connect

# เชื่อมต่อกับ MQTT Broker
client.connect(mqtt_broker, mqtt_port, 60)

# ทำการเชื่อมต่อและส่งข้อมูลไปที่ MQTT Broker
client.loop_forever()
