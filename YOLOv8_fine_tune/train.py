from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results =  model.train(data = "data_train/data.yaml",epochs = 1,imgsz = 640,batch =16, project = "run_yolov8",name = "exp_yolov8_")