import cv2
import time
import datetime


# cvlc v4l2:///dev/video5 --sout '#transcode{vcodec=h264,acodec=none}:rtp{sdp=rtsp://:8554/}'
# กำหนด URL ของกล้องผ่าน RTSP
rtsp_url = "rtsp://192.168.194.242:8554/"

# เปิดการเชื่อมต่อกับกล้อง
cap = cv2.VideoCapture(rtsp_url)

# กำหนดขนาดของวิดีโอ
frame_width = 640
frame_height = 480
frame_rate = 15

#ที่อยู่ของ mp4 และ video ที่ถูกบันทึก
output_mp4AndJpg_path = '/home/linaro/AIS_webcam/Photo_and_Video/'

# กำหนดระยะเวลาหน่วงระหว่างการบันทึก snapshot (วินาที)
snapshot_interval_P1 = 1 #ทุกๆ 1 วิ
snapshot_interval_P2 = 180 #ทุกๆ 3 นาที
last_snapshot_time = 0

# ตรวจสอบว่าเชื่อมต่อกล้องสำเร็จหรือไม่
if not cap.isOpened():
    print("ไม่สามารถเชื่อมต่อกล้องได้")
    exit()

recording = False
out = None


while True:
    # อ่านเฟรมภาพจากกล้อง
    ret, frame = cap.read()

    # รับวันที่และเวลาปัจจุบัน
    current_datetime = datetime.datetime.now()
    # แปลงวันที่และเวลาเป็นสตริงแบบกำหนดรูปแบบ
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    if not ret:
        print("เกิดข้อผิดพลาดในการอ่านเฟรมภาพ")
        break
    # แสดงภาพที่ได้จากกล้อง
    cv2.imshow("Camera Steaming", frame)

    #รอรับคำสั่งจากผู้ใช้
    if cv2.waitKey(1) & 0xFF == ord('o') and not recording:
        # เริ่มบันทึกวิดีโอ
        snapshot_counter = 0
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter(output_mp4AndJpg_path + f'Video_{formatted_datetime}.mp4', fourcc, frame_rate, (frame_width, frame_height))
        recording = True
        print("Start recording")
        
    elif cv2.waitKey(1) & 0xFF == ord('k') and recording:
        # หยุดบันทึกวิดีโอ
        if out is not None:
            out.release()
            recording = False
            snapshot_interval_P1 = 1 #ทุกๆ 1 วิ
            snapshot_interval_P2 = 180 #ทุกๆ 3 นาที
            last_snapshot_time = 0
            print("Stop recording")
            print("SnapShot Success")

    if recording == True :
        out.write(frame)
        if snapshot_counter < 20:
            current_time = time.time()  # เวลาปัจจุบัน
            if current_time - last_snapshot_time >= snapshot_interval_P1:
                snapshot_path = f"snapshot_{formatted_datetime}_{snapshot_counter+1}.jpg"
                cv2.imwrite(output_mp4AndJpg_path + snapshot_path, frame)
                snapshot_counter += 1
                last_snapshot_time = current_time  # อัปเดตเวลาของ snapshot ล่าสุด
                print(f"Saved snapshot: {snapshot_path}")
        
        elif snapshot_counter >= 20:
            current_time = time.time()  # เวลาปัจจุบัน
            if current_time - last_snapshot_time >= snapshot_interval_P2:
                snapshot_path = f"snapshot_{formatted_datetime}_{snapshot_counter+1}.jpg"
                cv2.imwrite(output_mp4AndJpg_path + snapshot_path, frame)
                snapshot_counter += 1
                last_snapshot_time = current_time  # อัปเดตเวลาของ snapshot ล่าสุด
                print(f"Saved snapshot: {snapshot_path}")

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Disconnect Camera")
        break

# คืนทรัพยากร
cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()