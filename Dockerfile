# Use slim Python 3.10 base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (without torch/torchvision)
RUN pip install --no-cache-dir -r requirements.txt

# Install CPU-only PyTorch + torchvision separately
RUN pip install --no-cache-dir torch==2.10.0 torchvision==0.25.0 --index-url https://download.pytorch.org/whl/cpu

# Copy project files
COPY . .

# Set the port Hugging Face expects
ENV PORT=7860

# Launch FastAPI
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]