import cv2
import json
from custom_ultralytics_1 import ParkingManagement

# Video capture
cap = cv2.VideoCapture("resource/videoplayback.mp4")
assert cap.isOpened(), "Error reading video file"

# Video writer
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
video_writer = cv2.VideoWriter("parking management.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))


def combine_points_files(file1, file2, output_file):
    points_combined = []

    # file 1
    with open(file1, 'r') as f:
        data1 = json.load(f)
        if isinstance(data1, list):
            points_combined.extend(data1)

    #file 2
    with open(file2, 'r') as f:
        data2 = json.load(f)
        if isinstance(data2, list):
            points_combined.extend(data2)

    with open(output_file, 'w') as f:
        json.dump(points_combined, f, indent=4)


combine_points_files('bounding_boxes.json', 'bounding_boxes_2.json', 'all_points.json')


# Initialize parking management object
parkingmanager = ParkingManagement(
    model="runs/detect/train/weights/best.pt",  # path to model file
    json_file="all_points.json",  # path to parking annotations file
    conf = 0.3,
    show=False,
)

while cap.isOpened():
    ret, im0 = cap.read()
    if not ret:
        break

    results = parkingmanager(im0)

    #print(results)  # access the output

    video_writer.write(results.plot_im)  # write the processed frame.

cap.release()
video_writer.release()
cv2.destroyAllWindows()