from inference_sdk import InferenceHTTPClient
import cv2
import json

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="9adk5aYWcYN7UIzQBKWA"
)

image_path = "resource/"

result = CLIENT.infer(image_path, model_id="parking-detection-jeremykevin/8")


img = cv2.imread(image_path)
data = []

for detection in result['predictions']:
    center_x = int(detection['x'])
    center_y = int(detection['y'])
    width = int(detection['width'])
    height = int(detection['height'])

    x1 = int(center_x - width / 2)
    y1 = int(center_y - height / 2)
    x2 = int(center_x + width / 2)
    y2 = int(center_y + height / 2)

    cv2.rectangle(img, (x1,y1), (x2, y2), (0, 0, 255), 1)

    cv2.circle(img, (center_x, center_y), 4, (0, 0, 255), -1)


    item = {
            "points": [
                [x1, y1],
                [x2, y1],
                [x2, y2],
                [x1, y2]
            ]
        }

    data.append(item)


with open("points.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

cv2.imshow("image",img)

cv2.imwrite('resource/bbox_img.jpg', img)

cv2.waitKey(0)
cv2.destroyAllWindows()


