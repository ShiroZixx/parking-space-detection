from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.pt")  # build a new model from YAML

# Train the model
results = model.train(data="train_data/cars.yaml", epochs=50, imgsz=1920)
