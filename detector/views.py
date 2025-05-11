from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2
from .detector import detect_emotion

def index(request):
    return render(request, 'index.html')

def video_feed(request):
    cap = cv2.VideoCapture(0)

    def gen():
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = detect_emotion(frame)
            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
    
    return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')
