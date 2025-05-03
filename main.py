import cv2
import pickle
import numpy as np
import tkinter as tk
from tkinter import filedialog

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Chọn file video hoặc ảnh",
        filetypes=[("Tất cả", "*.*"), ("Video files", "*.mp4;*.avi"), ("Image files", "*.jpg;*.png")],
    )
    return file_path

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Không thể mở video. Vui lòng kiểm tra đường dẫn!")
        exit()

    try:
        with open('CarParkPos', 'rb') as f:
            posList = pickle.load(f)
    except:
        print("Không tìm thấy file 'CarParkPos'.")

    font = cv2.FONT_HERSHEY_COMPLEX_SMALL

    empty = 0.044

    rec = [(160,55),(125,55),(140,57),(115,57)]

    def parking_space_counter(img_processed):
        global counter
        counter = 0
        for position in posList:
            x, y = position
            if x < 300:
                width, height = rec[0]
            elif 400 < x < 700 or 1300 < x < 1650:
                width, height = rec[1]
            elif 700 < x < 800 or 1200 < x < 1300 or 1650 < x:
                width, height = rec[2]
            elif 800 < x < 1200:
                width, height = rec[3]

            full = width * height
            img_crop = img_processed[y:y + height, x:x + width]
            count = cv2.countNonZero(img_crop)
            ratio = count / full

            if ratio < empty:
                color = (0, 255, 0)
                counter += 1
            else:
                color = (0, 0, 255)

            color = (0, 255, 0) if ratio < empty else (0, 0, 255)

            cv2.rectangle(overlay, position, (position[0] + width, position[1] + height), color, -1)
            cv2.putText(overlay, "{:.3f}".format(ratio), (x + 4, y + height - 4), font, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

    paused = False

    while True:
        if not paused:
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()
            if not ret:
                print("Không thể đọc video.")
                break

            overlay = frame.copy()
            img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
            img_thresh = cv2.adaptiveThreshold(
                img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16
            )

            #cv2.imwrite('Gaussian.jpg', img_blur)
            #cv2.imwrite('Gray.jpg', img_gray)
            #cv2.imwrite('Thresh.jpg', img_thresh)
            #cv2.imwrite('Canny.jpg', img_edges)

            parking_space_counter(img_thresh)

            alpha = 0.7
            frame_new = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

            w, h = 220, 60
            cv2.rectangle(frame_new, (0, 0), (w, h), (255, 0, 255), -1)
            cv2.putText(
                frame_new, f"{counter}/{len(posList)}", (int(w / 10), int(h * 3 / 4)), font, 2, (255, 255, 255), 2
            )
            cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
            cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        cv2.imshow("frame", frame_new)
        #cv2.imshow('image_blur', img_blur)
        #cv2.imshow('image_thresh', img_thresh)


        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC để thoát
            break
        elif key == 32:  # Space để tạm dừng/chạy
            paused = not paused

    cap.release()
    cv2.destroyAllWindows()

# Chương trình chính
if __name__ == "__main__":
    file_path = select_file()
    if file_path:
        if file_path.lower().endswith((".mp4", ".avi")):  
            process_video(file_path)
        else:
            print("Định dạng file không được hỗ trợ.")
    else:
        print("Không có file nào được chọn.")
        