import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
import datetime
import os

# --- Cấu hình Của Bạn ---
# Tên file JSON xác thực tài khoản dịch vụ của bạn
# Đảm bảo file này nằm cùng thư mục với script
SERVICE_ACCOUNT_FILE = '/home/phung/Desktop/ALPR_OCR/gen-lang-client-0692198862-ac0a53711edc.json' 
# URL đầy đủ của Google Sheet bạn muốn ghi dữ liệu vào
# Đảm bảo Google Sheet này đã được chia sẻ với tài khoản dịch vụ
# Ví dụ: 'https://docs.google.com/spreadsheets/d/1pjqIxLiJzIi4xnz5mlt3ts4nSP9ZTYGvnAlySQgSOYA/edit#gid=1108826699'
GOOGLE_SHEET_URL = 'https://docs.google.com/spreadsheets/d/1hpQLlU01FOlE0LLzTUpjQ_8LA6Vj8CIMCsjS8FIJNfA/edit?gid=0#gid=0'

# Tên của worksheet trong Google Sheet (ví dụ: 'Sheet1' hoặc 'Training_Results')
WORKSHEET_NAME = 'BM_Data' 

# Đường dẫn đến thư mục chứa kết quả huấn luyện (ví dụ: runs/train/expX)
# THAY THẾ 'runs/train/exp' BẰNG ĐƯỜNG DẪN CHÍNH XÁC CỦA BẠN
# Ví dụ: nếu kết quả của bạn ở 'runs/train/exp5', hãy đặt là 'runs/train/exp5'
YOLOV5_RESULTS_DIR = '/home/phung/Desktop/ALPR_OCR/run_yolov8/exp_yolov8_agu_fog' # Ví dụ: Cần thay thế exp bằng tên thư mục cụ thể của bạn (exp1, exp2...)

def upload_yolov5_results_to_sheet():
    """
    Đọc kết quả YOLOv5 từ file results.csv và tải lên Google Sheet.
    """
    results_csv_path = os.path.join(YOLOV5_RESULTS_DIR, 'results(8).csv')

    if not os.path.exists(results_csv_path):
        print(f"Lỗi: Không tìm thấy file results.csv tại '{results_csv_path}'.")
        print("Vui lòng kiểm tra lại đường dẫn YOLOV5_RESULTS_DIR và tên file.")
        return

    try:
        # Đọc file results.csv
        df_results = pd.read_csv(results_csv_path)

        if df_results.empty:
            print(f"Lỗi: File results.csv tại '{results_csv_path}' trống rỗng.")
            return

        # Lấy hàng cuối cùng (thường là kết quả của epoch cuối cùng)
        latest_metrics = df_results.iloc[-1].to_dict()

    # Tăng số thứ tự trước khi tạo dictionary cho lần upload này
       
        # Chuẩn bị dữ liệu để đưa lên Google Sheet
        # Đảm bảo các khóa khớp với tên cột bạn muốn trên Google Sheet
        data_to_upload = {

            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'model_name': 'YOLOv8n', # Có thể thay đổi nếu bạn biết tên model cụ thể
            'epochs_trained': latest_metrics.get('epoch', 'N/A'),
            'train_time_sec': latest_metrics.get('time', 'N/A'), # Thêm cột thời gian huấn luyện
            'train_box_loss': latest_metrics.get('train/box_loss', 'N/A'),
            'train_cls_loss': latest_metrics.get('train/cls_loss', 'N/A'),
            'train_dfl_loss': latest_metrics.get('train/dfl_loss', 'N/A'), # Thêm dfl_loss
            'metrics_precision': latest_metrics.get('metrics/precision(B)', 'N/A'),
            'metrics_recall': latest_metrics.get('metrics/recall(B)', 'N/A'),
            'metrics_mAP50': latest_metrics.get('metrics/mAP50(B)', 'N/A'), # Đã cập nhật
            'metrics_mAP50_95': latest_metrics.get('metrics/mAP50-95(B)', 'N/A'), # Đã cập nhật
            'val_box_loss': latest_metrics.get('val/box_loss', 'N/A'),
            'val_cls_loss': latest_metrics.get('val/cls_loss', 'N/A'),
            'val_dfl_loss': latest_metrics.get('val/dfl_loss', 'N/A'), # Thêm val dfl_loss
            'dataset_version': 'exp_yolov8_agu_fog' # Cập nhật tên dataset của bạn
        }
        
        # Chuyển đổi thành DataFrame để dễ dàng upload
        df_upload = pd.DataFrame([data_to_upload])
        
        print("\nCollected Data to Upload:")
        print(df_upload.to_string(index=False))

        # --- Bắt đầu quá trình Upload lên Google Sheet ---
        gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
        # Sử dụng open_by_url để kết nối bằng link
        spreadsheet = gc.open_by_url(GOOGLE_SHEET_URL)
        
        try:
            worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
        except gspread.exceptions.WorksheetNotFound:
            print(f"Worksheet '{WORKSHEET_NAME}' không tìm thấy. Đang tạo worksheet mới...")
            worksheet = spreadsheet.add_worksheet(title=WORKSHEET_NAME, rows="500", cols="30")
        
        # Kiểm tra xem worksheet có tiêu đề chưa
        existing_values = worksheet.get_all_values()
        
        if not existing_values or len(existing_values[0]) < len(df_upload.columns):
            # Nếu worksheet trống hoặc số cột header hiện tại ít hơn số cột dữ liệu,
            # ghi cả header và dữ liệu từ hàng 1
            print(f"Worksheet '{WORKSHEET_NAME}' trống hoặc cần cập nhật header. Đang tải lên với header...")
            set_with_dataframe(worksheet, df_upload, row=1, col=1, include_index=False, include_column_header=True)
        else:
            # Nếu đã có header, chỉ ghi thêm dữ liệu vào hàng cuối cùng
            next_row = len(existing_values) + 1
            print(f"Worksheet '{WORKSHEET_NAME}' đã có dữ liệu. Đang thêm vào từ hàng {next_row} (không có header)...")
            set_with_dataframe(worksheet, df_upload, row=next_row, col=1, include_index=False, include_column_header=False)
            
        print(f"Dữ liệu đã được tải lên Google Sheet '{GOOGLE_SHEET_URL}', Worksheet '{WORKSHEET_NAME}' thành công.")

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Lỗi: Không tìm thấy Google Sheet theo URL '{GOOGLE_SHEET_URL}'. Vui lòng kiểm tra lại URL và quyền chia sẻ cho '{SERVICE_ACCOUNT_FILE}'.")
    except Exception as e:
        print(f"Đã xảy ra lỗi không mong muốn: {e}")

if __name__ == "__main__":
    print("Bắt đầu script tải lên kết quả YOLOv5...")
    upload_yolov5_results_to_sheet()
    print("Script đã hoàn thành.")
