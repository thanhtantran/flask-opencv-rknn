# RKNN Object detection 1 core with RK3566, running on browser with Flask

Tested SBC: 
- [Orange Pi 3B](https://orangepi.net/product-tag/orange-pi-3b)
- [Orange Pi CM4](https://orangepi.vn/shop/orange-pi-cm4-phien-ban-1g8gb)

This code is a new version of my old code [rknn-single-thread-3566](https://github.com/thanhtantran/rknn-single-thread-3566) 

Instruction to run

Clone the code
```
admin@orangepi3b:~$ git clone https://github.com/thanhtantran/flask-opencv-rknn && cd flask-opencv-rknn
```

Install python pip and venv
```
admin@orangepi3b:~$ sudo apt install python3-venv python3-pip -y
```

Check your python version
```
admin@orangepi3b:~$ python3 --version
Python 3.10.12
```

Download the specific rknn-toolkit-lite2 1.5.2 for your python version. (Pls note that new  rknn-toolkit-lite2 2.3.0 will not work since the model is converted base on old rknn-toolkit2)
```
wget https://github.com/airockchip/rknn-toolkit2/raw/refs/heads/v1.5.2/rknn_toolkit_lite2/packages/rknn_toolkit_lite2-1.5.2-cp310-cp310-linux_aarch64.whl
pip install rknn_toolkit_lite2-2.3.0-cp310-cp310-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
pip install flask opencv-contrib-python 
```

Check rknn-toolkit-lite2 version
```
admin@orangepi3b:~/flask-opencv-rknn$ pip list | grep rknn-toolkit-lite2
rknn-toolkit-lite2    1.5.2
```

Copy the library
```
wget https://github.com/airockchip/rknn-toolkit2/raw/refs/heads/master/rknpu2/runtime/Linux/librknn_api/aarch64/librknnrt.so && sudo cp librknnrt.so /usr/lib
```

Then run the inference
```
python main.py
```

The app will run on http://YOUR_ORANGEPI_IP:5000 Please open browser and navigate to it.

![flask-rknn-object-detection](https://github.com/user-attachments/assets/90806c89-2466-4349-93ce-f9c2a9147628)

The default username and password is orangepi/orangepi.vn

You can Record / Ghi hình or Nhận diện / Run Detection. Thoát / Logout

![flask-rknn-object-detection2](https://github.com/user-attachments/assets/ed86a3b3-94f7-44fa-aec5-6ff7d4c1d239)


# Reference

https://github.com/miguelgrinberg/flask-video-streaming

https://gitee.com/Embedfire/flask-video-streaming-recorder

https://github.com/thanhtantran/rknn-single-thread-3566

https://github.com/airockchip/rknn-toolkit2

https://github.com/airockchip/rknn-toolkit2/

