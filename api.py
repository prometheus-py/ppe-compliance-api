from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from ultralytics import YOLO
import shutil
import os
import time
import uuid
import cv2

app = FastAPI()

# Load model once at startup (CPU only)
model = YOLO("ppe_model.pt")
model.to("cpu")


@app.get("/")
def health_check():
    return {"status": "PPE API is running"}


@app.post("/detect")
async def detect(file: UploadFile = File(...)):

    # Generate unique filenames
    temp_filename = f"/tmp/temp_{uuid.uuid4().hex}.jpg"
    annotated_filename = f"/tmp/annotated_{uuid.uuid4().hex}.jpg"

    # Save uploaded image
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    start_time = time.time()

    # Run inference (explicit CPU + reduced size for memory safety)
    results = model.predict(
        source=temp_filename,
        conf=0.4,
        imgsz=640,
        device="cpu"
    )

    inference_time = round(time.time() - start_time, 3)

    # Load image for annotation
    image = cv2.imread(temp_filename)

    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        class_name = model.names[cls_id]
        xyxy = box.xyxy[0].tolist()

        x1, y1, x2, y2 = map(int, xyxy)

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.putText(
            image,
            f"{class_name} {conf:.2f}",
            (x1, max(y1 - 10, 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    # Save annotated image
    cv2.imwrite(annotated_filename, image)

    # Cleanup original file
    os.remove(temp_filename)

    return FileResponse(
        annotated_filename,
        media_type="image/jpeg",
        filename="result.jpg",
        headers={"X-Inference-Time": f"{inference_time}s"}
    )