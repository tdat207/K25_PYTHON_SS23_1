"""
Phân tích giải pháp:
- Chuyển đổi công thức tính khoảng cách thô sơ cũ sang công thức Haversine chuẩn để tính toán chính xác theo km trên mặt cầu.
- Thay thế 'from math import *' thành import tường minh từng hàm: sin, cos, sqrt, atan2, radians để tránh ô nhiễm bộ nhớ.
- Sửa lỗi sập chương trình FileExistsError bằng cách dùng os.path.exists() kiểm tra thư mục logs trước khi gọi os.mkdir().
- Đổi các tên biến tối nghĩa s, x, y, d thành tên tiếng Anh chuẩn sạch: shipment, distance, depart_time, eta.
"""

from math import sin, cos, sqrt, atan2, radians
import os
import datetime


shipments = [
    {"id": "TRK-001", "from_lat": 21.0285, "from_lon": 105.8542, "to_lat": 10.8231, "to_lon": 106.6297, "depart": "2026-06-10 08:00:00", "deadline": "2026-06-11 12:00:00"}, 
    {"id": "TRK-002", "from_lat": 21.0285, "from_lon": 105.8542, "to_lat": 16.0544, "to_lon": 108.2022, "depart": "2026-06-10 09:30:00", "deadline": "2026-06-10 15:00:00"}, 
]

print("====== HỆ THỐNG ĐIỀU PHỐI RIKKEI LOGISTICS =======")
if not os.path.exists("logs"):
    os.mkdir("logs")
    print("[INFO] Khởi tạo hệ thống lưu trữ log hành trình... Thành công.")
else:
    print("[INFO] Hệ thống lưu trữ log hành trình đã sẵn sàng.")

print("-" * 75)
for shipment in shipments:
    earth_radius = 6371.0
    
    lat1 = radians(shipment["from_lat"])
    lon1 = radians(shipment["from_lon"])
    lat2 = radians(shipment["to_lat"])
    lon2 = radians(shipment["to_lon"])
    
    diff_lat = lat2 - lat1
    diff_lon = lon2 - lon1
    
    val_a = sin(diff_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(diff_lon / 2)**2
    val_c = 2 * atan2(sqrt(val_a), sqrt(1 - val_a))
    distance = earth_radius * val_c
    
    try:
        depart_time = datetime.datetime.strptime(shipment["depart"], "%Y-%m-%d %H:%M:%S")
        deadline = datetime.datetime.strptime(shipment["deadline"], "%Y-%m-%d %H:%M:%S")
        
        # Giả định xe chạy vận tốc cố định 60km/h
        hours_needed = distance / 60
        eta = depart_time + datetime.timedelta(hours=hours_needed)
        
        print(f"[CHUYẾN XE {shipment['id']}]")
        print(f" + Khoảng cách vận chuyển: {distance:.2f} km")
        print(f" + Thời gian khởi hành: {shipment['depart']}")
        print(f" + Dự kiến cập bến (ETA): {eta.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if eta <= deadline:
            print(" + Trạng thái: 🟢 AN TOÀN (Kịp tiến độ trước deadline)\n")
        else:
            print(f" + Trạng thái: 🔴 CẢNH BÁO (Trễ hạn! Deadline yêu cầu lúc {deadline.strftime('%H:%M:%S')})\n")
            
    except ValueError:
        print(f"Lỗi: Chuyến xe {shipment['id']} dính sai định dạng chuỗi thời gian!\n")
        continue

print("========================================================")