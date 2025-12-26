import cv2
import threading
import time
from controller.utils.rknn_image import *

RTSP_URL = "rtsp://admin:password@192.168.10.27:554/h264_stream"

class RecordingThread(threading.Thread):
    def __init__(self, name, camera):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True

        self.cap = camera
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter('./video.avi', fourcc, 20.0, (640, 640))

    def run(self):
        while self.isRunning:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
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
            raise RuntimeError('Could not open video.')

        # Create RKNN object
        self.rknn_lite = RKNNLite()
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

        width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(f"Actual resolution: {width}x{height}")

        self.recordingThread = None
        self.is_record = False
        self.out = None

        self.image = None
        self.rknn_frame = None
        self.frame = None
        self.outputs = None

        self.processing_thread = None
        self.processed_frame = None
        self.is_process = False
        
        # load rknn
        self.load_rknn()

    def __del__(self):
        self.cap.release()
        self.rknn_lite.release()

    def get_frame(self):
        ret, self.frame = self.cap.read()
        if ret:
            self.frame = cv2.resize(self.frame, (640, 640))
            
            # Use the processed frame if available, otherwise use the original frame
            display_frame = self.processed_frame if self.is_process and self.processed_frame is not None else self.frame
            
            if display_frame is not None:
                ret, image = cv2.imencode('.jpg', display_frame)
                return image.tobytes()
        return None

    def start_process(self):
        self.is_process = True
        if self.processing_thread is None or not self.processing_thread.is_alive():
            self.processing_thread = threading.Thread(target=self.rknn_process, daemon=True)
            self.processing_thread.start()

    def stop_process(self):
        self.is_process = False
        self.processed_frame = None

    def rknn_process(self):
        while self.is_process:
            if self.frame is not None:
                # Create a copy of the frame to avoid race conditions
                current_frame = self.frame.copy()
                
                # Process the frame
                image = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
                outputs = self.rknn_lite.inference(inputs=[image])
                
                # Only update processed_frame if we're still processing
                if self.is_process:
                    self.processed_frame = process_image(image, outputs)
            
            # Add a small sleep to prevent CPU overuse
            time.sleep(0.01)

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


            
