import gradio as gr
import requests
import io
from PIL import Image

API_URL = "https://prometheus-ai-ppe-api.hf.space/detect"

def detect_ppe(image):
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    buf.seek(0)

    files = {"file": ("image.jpg", buf, "image/jpeg")}
    response = requests.post(API_URL, files=files)

    if response.status_code == 200:
        return Image.open(io.BytesIO(response.content))
    else:
        return None

interface = gr.Interface(
    fn=detect_ppe,
    inputs=gr.Image(type="pil"),
    outputs=gr.Image(type="pil"),
    title="PPE Detection",
    description="Upload an image to detect Helmet and Vest"
)

interface.launch()