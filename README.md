# ALPR_Project
Phần I: Giới thiệu:
- Đây là dự án tự động nhận diện biển số xe (ALPR).
- Dự án được public có thể chỉnh sửa mở rộng thêm tùy thích.
- Chủ yếu sử dụng mô hình yolov8 để thực hiện
- Tải project về máy (download project): git clone https://github.com/20PhungTran21/ALPR_Project.git

Phần I: cài đặt thư viện và các gói liên quan đến mô hình (import library):
- Cài đặt thư viện ultralytics: pip install ultralytics -> dùng để làm việc với mô hình yolo
- Cài đặt thư viện gspread: pip install gspread -> Dùng để kết nối với googlesheet API 
- Cài đặt thu viện pandas: pip install pandas -> Dùng làm việc với dữ liệu (CSV, Excel, ...)
- Cài đặt thư viện opencv: pip install opencv-python -> Dùng để xử lý ảnh và thị giác máy tình.

Phần II: Huấn luyện mô hình (trainning model):
- Chuẩn bị tập dữ liệu: link tham khảo nếu chưa có https://universe.roboflow.com/ansrt/pd-rt/dataset/1
- Tùy thuộc vào muốn training theo mô hình nào ở đây mô hình sử dụng là yolov8 nên sẽ tải định dạng file của yolov8 về máy.
- Sau đó vào file train.py thay dường dẫn thư mục data = "..." thay bằng đường dẫn data mới tải về của cá nhân bằng đường dẫn data = "....yaml" của mình và bắt đầu thực hiện training.
- Đây chỉ là bước cơ bản ta huấn luyên mô hình sẽ sử dụng thêm các agumentations (tăng cường thêm dữ liệu) để hợp với thực tế hơn