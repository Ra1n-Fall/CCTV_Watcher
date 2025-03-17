import numpy as np
import cv2 as cv
import os

script_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 실행 중인 파일의 경로
savedvideo = os.path.join(script_dir, "savedvideo.avi")  # 같은 폴더에 저장

VideoCapture = cv.VideoCapture("rtsp://210.99.70.120:1935/live/cctv001.stream")
VideoWriter = cv.VideoWriter()
if VideoCapture.isOpened():
    isVideoRecording = False
    contrast = 1.6
    contrast_step = 0.1
    brightness = -40
    brightness_step = 1

    while True:
        ##비디오 읽기
        isVideoReading, img = VideoCapture.read()
        if not isVideoReading:
            break
        ##비디오 프레임 가져오기 
        frame = VideoCapture.get(cv.CAP_PROP_POS_FRAMES)
        waitmsec = 1/frame*1000
        
        key = cv.waitKey(int(waitmsec))
        ##비디오 녹화
        
        if not VideoWriter.isOpened():
            h, w, *_ = img.shape
            is_color = (img.ndim > 2) and (img.shape[2] > 1)
            VideoWriter.open(savedvideo, cv.VideoWriter_fourcc(*'XVID'), frame, (w, h), is_color)

        img = contrast * img + brightness
        img[img > 255] = 255
        img[img < 0] = 0
        img = img.astype(np.uint8)
        
        if(isVideoRecording):
                VideoWriter.write(img)
        ##키보드 입력 처리
        if key == ord(' ') and isVideoRecording:
            isVideoRecording = False
            print("Video recording is stopped")
        elif key == ord(' ') and not isVideoRecording:
            isVideoRecording = True
            print("Video recording is started")
        elif key == 27:
            break
        elif key == ord('+') or key == ord('='):
            contrast += contrast_step
        elif key == ord('-') or key == ord('_'):
            contrast -= contrast_step
        elif key == ord(']') or key == ord('}'):
            brightness += brightness_step
        elif key == ord('[') or key == ord('{'):
            brightness -= brightness_step
        ##UI 출력
        pos = (70, 50)
        if(isVideoRecording):
            cv.circle(img, pos, radius=30, color=(0, 0, 255), thickness=-1)
        else:
            cv.circle(img, pos, radius=30, color=(0, 255, 0), thickness=-1)
        ##비디오 출력
        cv.imshow("Video", img)
    VideoWriter.release()
    cv.destroyAllWindows()
    