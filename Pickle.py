import cv2
import pickle
import tkinter as tk
from tkinter import filedialog

rec = [(160,55),(125,55),(140,57),(115,57)]
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

# Đọc ảnh
def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Chọn file video hoặc ảnh",
        filetypes=[("Tất cả", "*.*"), ("Video files", "*.mp4;*.avi"), ("Image files", "*.jpg;*.png")],
    )
    return file_path

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))

    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            for r in rec:
                if x1 < x < x1 + r[0] and y1 < y < y1 + r[1]:
                    posList.pop(i)

    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

#print(posList)
file_path = select_file()

while True:
    img = cv2.imread(file_path)
    cv2.putText(img, "LMB: Add position, RMB: Remove, ESC: Exit", (20, 50), font, 1, (0, 255, 255),1)

    for pos in posList:
        x,y = pos
        if x < 300:
            cv2.rectangle(img, pos, (x + rec[0][0], y + rec[0][1]), (255, 0, 255), 2)
        if 400 < x < 700 or 1300 < x < 1650:
            cv2.rectangle(img, pos, (x + rec[1][0], y + rec[1][1]), (255, 0, 255), 2)
        if 700 < x < 800 or 1200 < x < 1300 or 1650 < x:
            cv2.rectangle(img, pos, (x + rec[2][0], y + rec[2][1]), (255, 0, 255), 2)
        if 800 < x < 1200:
            cv2.rectangle(img, pos, (x + rec[3][0], y + rec[3][1]), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    if cv2.waitKey(1) & 0xFF == 27:
        break
