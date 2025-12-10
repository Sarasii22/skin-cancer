FROM python:3.11-slim

# Install system deps for WeasyPrint (PDF generation) + clean up
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 libpangoft2-1.0-0 libjpeg-dev libopenjp2-7 libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Install all other packages (without torch)
RUN pip install --no-cache-dir --timeout=300 -r requirements.txt

# Install CPU-only Torch (small & fast – no CUDA timeouts)
RUN pip install --no-cache-dir --timeout=300 torch torchvision --index-url https://download.pytorch.org/whl/cpu

COPY app ./app
COPY models ./models
COPY templates ./templates

RUN mkdir -p /app/results
VOLUME /app/results

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]