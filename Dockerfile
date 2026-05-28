FROM python:3.11-slim

# Install the ping utility
RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY monitor.py .

# Run Python unbuffered so logs stream instantly
CMD ["python", "-u", "monitor.py"]
