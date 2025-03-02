import cv2
import threading
import time
from controller.utils.rknn_image import *

class RecordingThread(threading.Thread):
    def __init__(self, name, camera):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True

        self.cap = camera
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter('./controller/static/video.avi', fourcc, 20.0, (640, 640))

    def run(self):
        while self.isRunning:
            ret, frame = self.cap.read()
            if ret:
                self.out.write(frame)

        self.out.release()

    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.out.release()

class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError('Could not open camera.')

        # Create RKNN object
        self.rknn_lite = RKNNLite()

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

        self.recordingThread = None
        self.is_record = False
        self.out = None

        self.image = None
        self.rknn_frame = None
        self.frame = None
        self.outputs = None

        self.is_process= False

        # load rknn
        self.load_rknn()

    def __del__(self):
        self.cap.release()
        self.rknn_lite.release()

    def get_frame(self):
        ret, self.frame = self.cap.read()
        if ret:
            if self.is_process:
                self.image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                self.image = cv2.resize(self.frame, (IMG_SIZE, IMG_SIZE))
                self.outputs = self.rknn_lite.inference(inputs=[self.image])
                self.frame = process_image(self.image, self.outputs)

            if self.frame is not None:
                ret, image = cv2.imencode('.jpg', self.frame)
                return image.tobytes()
        else:
            return None

    def start_record(self):
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.cap)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False

        if self.recordingThread != None:
            self.recordingThread.stop()

    def load_rknn(self):
        # load RKNN model
        print('--> Load RKNN model')
        ret = self.rknn_lite.load_rknn(RKNN_MODEL)
        if ret != 0:
            print('Load RKNN model failed')
            exit(ret)
        # Init runtime environment
        print('--> Init runtime environment')
        ret = self.rknn_lite.init_runtime()
        if ret != 0:
            print('Init runtime environment failed!')
            exit(ret)

    def start_process(self):
        self.is_process = True
        #threading.Thread(target=self.rknn_process, daemon=True, args=()).start()

    def stop_process(self):
        self.is_process = False
        #self.outputs = None
        #self.image = None

    def rknn_process(self):
        if self.is_process:
            print('--> is_process true')
            self.outputs = self.rknn_lite.inference(inputs=[self.frame])
        else:
            self.outputs = None


            
