import cv2
import time
from ultralytics import YOLO

# ==== CẤU HÌNH ====
model_path = YOLO('/home/phung/Desktop/ALPR_Project/run_yolov8/exp_yolov8_2/weights/best.pt')           # mô hình đã fine-tune
video_path = "/home/phung/Desktop/ALPR_Project/carLicence4.mp4"         # đường dẫn video hoặc ảnh
use_video = True                 # True = video / webcam, False = ảnh tĩnh
conf_threshold = 0.3
# ===================

# Load mô hình
model = YOLO(model_path)
# Đọc ảnh hoặc video
cap = cv2.VideoCapture(0 if video_path == "webcam" else video_path)
font = cv2.FONT_HERSHEY_SIMPLEX

total_frames = 0
total_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    start_time = time.time()
    results = model(frame, conf=conf_threshold)
    end_time = time.time()

    total_frames += 1
    inference_time = end_time - start_time
    total_time += inference_time

    # Hiển thị kết quả
    result_frame = results[0].plot()

    # Tính metrics
    fps = total_frames / total_time if total_time > 0 else 0
    fpm = fps * 60
    latency = inference_time * 1000

    # Ghi thông tin lên ảnh
    cv2.putText(result_frame, f"FPS: {fps:.2f}", (10, 30), font, 0.8, (0, 255, 0), 2)
    cv2.putText(result_frame, f"FPM: {fpm:.2f}", (10, 60), font, 0.8, (255, 255, 0), 2)
    cv2.putText(result_frame, f"Latency: {latency:.2f} ms", (10, 90), font, 0.8, (0, 255, 255), 2)

    # Hiển thị cửa sổ
    cv2.imshow("YOLOv8 Inference + Metrics", result_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Nếu test ảnh tĩnh thì thoát sau 1 frame
    if not use_video:
        break

cap.release()
cv2.destroyAllWindows()
