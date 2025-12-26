from flask import session, render_template, request, redirect, url_for, Response, jsonify
from controller.modules.home import home_blu
from controller.utils.camera import VideoCamera
import time
import cv2

video_camera = None
global_frame = None

# Start
@home_blu.route('/')
def index():
    # Dang nhap
    username = session.get("username")
    if not username:
        return redirect(url_for("user.login"))
    return render_template("index.html")

# Lay video Stream
def video_stream():
    global video_camera
    global global_frame

    if video_camera is None:
        video_camera = VideoCamera()

    while True:
        #start_time = time.time()
        frame = video_camera.get_frame()
        
        #end_time = time.time()
        #print('get_frame cost %f second' % (end_time - start_time))
        #time.sleep(0.01)
        if frame is not None:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            # Check if global_frame is None before using it
            if global_frame is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')
            else:
                # Provide a default empty image or skip this iteration
                continue  # Skip this iteration if no frame is available


# Xem hinh
@home_blu.route('/video_viewer')
def video_viewer():
    # Check login ?
    username = session.get("username")
    if not username:
        return redirect(url_for("user.login"))
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# Ghi hinh
@home_blu.route('/record_status', methods=['POST'])
def record_status():
    username = session.get("username")
    if not username:
        return jsonify(error="unauthorized"), 401

    global video_camera
    if video_camera is None:
        video_camera = VideoCamera()

    payload = request.get_json(silent=True) or {}
    status = payload.get('status')

    if status == "true":
        file_name = video_camera.start_record()
        return jsonify(result="started", file_name=file_name)

    file_name = video_camera.stop_record()
    file_url = url_for('static', filename=f"recordings/{file_name}") if file_name else None
    return jsonify(result="stopped", file_name=file_name, file_url=file_url)


# Nhan dien
@home_blu.route('/process_status', methods=['POST'])
def process_status():
    username = session.get("username")
    if not username:
        return jsonify(error="unauthorized"), 401

    global video_camera
    if video_camera is None:
        video_camera = VideoCamera()

    payload = request.get_json(silent=True) or {}
    process_status = payload.get("status")

    if process_status == "true":
        video_camera.start_process()
        return jsonify(result="process")

    video_camera.stop_process()
    return jsonify(result="pause")
