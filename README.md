### PPE Compliance Detection API

YOLOv8-based object detection API for detecting Personal Protective Equipment (PPE) compliance in images. This project exposes a FastAPI endpoint that performs inference using a trained YOLOv8 model to detect:
 1. Helmet
 2. Safety Vest


### Live Frontend

Access the live Gradio interface globally:  
[https://prometheus-ai-ppe-api-ui.hf.space](https://prometheus-ai-ppe-api-ui.hf.space)

- No local setup needed — just upload an image and view the results online.


### Tech Stack
* Python 3.x
* FastAPI
* Uvicorn
* Ultralytics YOLOv8
* PyTorch
* OpenCVq


### Model Details

Architecture: YOLOv8 (Ultralytics)

Task: Object Detection

Classes:[helmet, vest]

Model file: `ppe_model.pt`
The model is pre-trained and fine-tuned for PPE detection

### Project Structure
ppe-compliance-api/

ppe-compliance-api/

│

├── backend/ # Backend API files

│ ├── api.py

│ ├── ppe_model.pt

│ ├── requirements.txt

│ └── Procfile

│

├── frontend/ # Frontend UI files

│ ├── app.py

│ └── requirements.txt

│

├── Dockerfile

├── README.md

└── .gitignore

Clone the repository:
`git clone https://github.com/prometheus-py/ppe-compliance-api.git`

`cd ppe-compliance-api`

Create virtual environment:
`python -m venv venv
venv\Scripts\activate`

Install dependencies:
`pip install -r requirements.txt`

### Running the API

Start the server:
`uvicorn api:app --reload`

API will run at:
`http://127.0.0.1:8000`

Swagger documentation available at:
`http://127.0.0.1:8000/docs`

📡 API Endpoint
POST /predict

Upload an image file for PPE detection.

### Use Case
This API can be integrated into:

-> CCTV monitoring systems

-> Industrial safety dashboards

-> Construction site compliance tools

-> Smart factory monitoring systems


# Key Notes

Designed for demonstration and portfolio purposes. For production deployment, consider:

* Docker containerization

* GPU-enabled inference

* Authentication layer

* Rate limiting

* Model versioning

### 👤 Author

# Khaled Been Shams
# Machine Learning & Computer Vision Enthusiast
