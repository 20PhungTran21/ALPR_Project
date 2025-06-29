from ultralytics import YOLO
import cv2

# ----------- CẤU HÌNH -------------
mode = input("input type image or video or webcam: ")       # Chọn: "image", "video", hoặc "webcam"
model_path = "/home/phung/Desktop/ALPR_Project/run_yolov8/exp_yolov8_no_agu/best(15).pt"  # Đường dẫn tới mô hình (có thể là best.pt nếu fine-tune)
image_path = "/home/phung/Desktop/ALPR_Project/data_train/test/images"
video_path = "/home/phung/Desktop/ALPR_Project/RECAP - ROADSHOW ＂MUA XE NEW - TRÚNG XẾ YÊU＂.mp4vid"
# ----------------------------------

# Tải model YOLO
model = YOLO(model_path)

if mode == "image":
    # Đọc và dự đoán ảnh
    results = model(image_path)
    res_plot = results[0].plot()
    cv2.imshow("YOLOv8 - Image", res_plot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

elif mode in ["video", "webcam"]:
    # Đọc video hoặc webcam
    cap = cv2.VideoCapture(0 if mode == "webcam" else video_path)

    # Lấy thông số video nếu muốn ghi lại
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    # Ghi video đầu ra nếu cần
    # out = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        res_plot = results[0].plot()

        cv2.imshow("YOLOv8 - Video/Webcam", res_plot)
        # out.write(res_plot)  # Bật nếu muốn lưu video

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    # out.release()
    cv2.destroyAllWindows()

else:
    print("Vui lòng chọn mode = 'image', 'video', hoặc 'webcam'")
