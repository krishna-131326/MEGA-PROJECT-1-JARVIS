FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for audio (optional if we mock in CI, but good for local)
RUN apt-get update && apt-get install -y \
    gcc \
    libasound-dev \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0 \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY src/ src/

# Install the package
RUN pip install --no-cache-dir .

# Command to run the assistant in text mode by default
CMD ["python", "-m", "jarvis.cli"]
