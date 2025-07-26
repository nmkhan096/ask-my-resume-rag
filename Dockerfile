# Defines a custom Docker image for the app

FROM python:3.10-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Use environment variable for port (defaults to 8501, Railway automatically sets PORT=8080)
ENV PORT=8501
EXPOSE ${PORT}

CMD ["sh", "-c", "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true"]