# ALPR_Project
Phần I: Giới thiệu:
- Đây là dự án tự động nhận diện biển số xe (ALPR).
- Dự án được public có thể chỉnh sửa mở rộng thêm tùy thích.
- Chủ yếu sử dụng mô hình yolov8 để thực hiện
- Tải project về máy (download project): git clone https://github.com/20PhungTran21/ALPR_Project.git

Phần II: cài đặt thư viện và các gói liên quan đến mô hình (import library):
- Cài đặt thư viện ultralytics: pip install ultralytics -> dùng để làm việc với mô hình yolo
- Cài đặt thư viện gspread: pip install gspread -> Dùng để kết nối với googlesheet API 
- Cài đặt thu viện pandas: pip install pandas -> Dùng làm việc với dữ liệu (CSV, Excel, ...)
- Cài đặt thư viện opencv: pip install opencv-python -> Dùng để xử lý ảnh và thị giác máy tình.
Phần III: Tập dữ liệu và tài nguyên thực hiện:
1. Dữ liệu huấn luyện
- Dữ liệu được sử dụng từ nguồn: Roboflow - PD & RT Dataset
- Định dạng: YOLOv8 format
- Tổng số ảnh: 1548
- Tập dữ liệu được chia theo tỷ lệ:
    + Train: 96% (1482 ảnh)
    + Validation: 3% (44 ảnh)
    + Test: 1% (22 ảnh)
2. Tài nguyên máy tính:
- Bộ xử lý (CPU):AMD Ryzen 3 5400U: 4 nhân, 8 luồng, Tốc độ cơ bản: 2.6 GHz.
- RAM: 24GB bus 2133MHz DUAL chanel
- GPU: card đồ họa tích hợp AMD Radeon Graphics.

Phần IV: Huấn luyện mô hình (trainning model):
- Chuẩn bị tập dữ liệu: link tham khảo nếu chưa có https://universe.roboflow.com/ansrt/pd-rt/dataset/1
- Tùy thuộc vào muốn training theo mô hình nào ở đây mô hình sử dụng là yolov8 nên sẽ tải định dạng file của yolov8 về máy.
- Sau đó vào file train.py thay dường dẫn thư mục data = "..." thay bằng đường dẫn data mới tải về của cá nhân bằng đường dẫn data = "... .yaml" của mình và bắt đầu thực hiện training.
- Đây chỉ là bước cơ bản ta huấn luyên mô hình sẽ sử dụng thêm các agumentations (tăng cường thêm dữ liệu) để hợp với thực tế hơn.

Phần V: Thử nghiệm khi có mô hình:
- Có thể thực hiện kiểm thử mô hình bằng file test.py. Cung cấp dữ liệu hình ảnh, video và camera để thử nghiệm
- Các lần thực hiện huấn luyên sẽ được lưu lại dưới dạng .pt
- Để trực quan hơn ta sẽ đưa dữ liệu lên google sheet để hiện thị kết quả benmark của từng lần huấn luyện, để đánh giá so sánh và cải tiến thêm. File upload_data.py dùng để kết nối làm việc với googlesheet thông qua key API link: https://console.cloud.google.com/apis, đăng ký và khởi tạo key API để tích hợp với cript. File này có dạng json. Thay thế SERVICE_ACCOUNT_FILE = Đường dẫn key api (lưu ý key nên nằm trên cùng thư mục với cript), GOOGLE_SHEET_URL là URL google của người dùng. Đọc thêm chú thích trong thư mục cript.