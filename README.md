[🇺🇸 English version](README-en.md)

# Nhận diện đối tượng RKNN (1 core) với RK3566, chạy trên trình duyệt bằng Flask

Bo mạch đã được kiểm thử:
- [Orange Pi 3B](https://orangepi.net/product-tag/orange-pi-3b)
- [Orange Pi CM4](https://orangepi.vn/shop/orange-pi-cm4-phien-ban-1g8gb)

Mã nguồn này là phiên bản mới của project cũ:
[rknn-single-thread-3566](https://github.com/thanhtantran/rknn-single-thread-3566)

![Demo](https://github.com/user-attachments/assets/73ec0602-6a74-4b0a-b6f5-aa77eea09b42)

---

## Hướng dẫn chạy chương trình

### Clone mã nguồn
```bash
git clone https://github.com/thanhtantran/flask-opencv-rknn
cd flask-opencv-rknn
```

### Cài đặt pip, venv và OpenCV
```bash
sudo apt install python3-venv python3-pip -y
sudo apt install -y python3-opencv
```

### Kiểm tra phiên bản Python
```bash
python3 --version
```
Ví dụ:
```
Python 3.10.12
```

### Tải và cài đặt rknn-toolkit-lite2 (phiên bản bắt buộc)
⚠️ **Lưu ý:** Phải dùng đúng phiên bản **rknn-toolkit-lite2 1.5.2**.  
Các phiên bản mới hơn sẽ **không hoạt động**, vì model được convert bằng rknn-toolkit2 cũ.

```bash
wget https://github.com/airockchip/rknn-toolkit2/raw/refs/heads/v1.5.2/rknn_toolkit_lite2/packages/rknn_toolkit_lite2-1.5.2-cp310-cp310-linux_aarch64.whl
pip install rknn_toolkit_lite2-1.5.2-cp310-cp310-linux_aarch64.whl
pip install flask opencv-contrib-python
```

### Kiểm tra phiên bản rknn-toolkit-lite2
```bash
pip list | grep rknn-toolkit-lite2
```
Kết quả mong đợi:
```
rknn-toolkit-lite2    1.5.2
```

### Tạo thư mục và tải model
```bash
mkdir models && cd models
wget https://github.com/thanhtantran/rknn-single-thread-3566/raw/refs/heads/main/yolov5s.rknn
```

### Sao chép thư viện runtime
```bash
wget https://github.com/airockchip/rknn-toolkit2/raw/refs/heads/master/rknpu2/runtime/Linux/librknn_api/aarch64/librknnrt.so
sudo cp librknnrt.so /usr/lib
```

### Chạy chương trình nhận diện
```bash
python main.py
```

Ứng dụng sẽ chạy tại:
http://IP_ORANGE_PI:5000

Mở trình duyệt và truy cập địa chỉ trên.

![Giao diện Flask RKNN](https://github.com/user-attachments/assets/6c2598ff-78f3-4596-994f-aa420f06dba6)

---

## Thông tin đăng nhập mặc định
- **Username:** orangepi  
- **Password:** orangepi.vn  

Chức năng:
- **Record / Ghi hình**
- **Run Detection / Nhận diện**
- **Logout / Thoát**

![Giao diện điều khiển](https://github.com/user-attachments/assets/1dd485f5-9eb5-4a05-91cf-1fc7f7e574ef)

---

## Tham khảo
- https://github.com/miguelgrinberg/flask-video-streaming  
- https://gitee.com/Embedfire/flask-video-streaming-recorder  
- https://github.com/thanhtantran/rknn-single-thread-3566  
- https://github.com/airockchip/rknn-toolkit2  
