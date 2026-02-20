from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from ultralytics import YOLO
import shutil
import os
import time
import uuid
import cv2

app = FastAPI()

# Load trained model
model = YOLO("ppe_model.pt")


@app.post("/detect")
async def detect(file: UploadFile = File(...)):

    # Create unique filename for uploaded image
    temp_filename = f"temp_{uuid.uuid4().hex}.jpg"

    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    start_time = time.time()

    # Run inference
    results = model(temp_filename, conf=0.4)

    inference_time = time.time() - start_time

    # Load image for annotation
    image = cv2.imread(temp_filename)

    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        class_name = model.names[cls_id]
        xyxy = box.xyxy[0].tolist()

        x1, y1, x2, y2 = map(int, xyxy)

        # Draw bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Label text
        cv2.putText(
            image,
            f"{class_name} {conf:.2f}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    # Save annotated image
    annotated_filename = f"annotated_{uuid.uuid4().hex}.jpg"
    cv2.imwrite(annotated_filename, image)

    # Remove original uploaded image
    os.remove(temp_filename)

    # Return annotated image directly
    return FileResponse(
        annotated_filename,
        media_type="image/jpeg",
        filename="result.jpg"
    )