## Pull prebuilt Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy your local files into the container
COPY . /app

# Install required tools (git, build-essential, etc.)
RUN apt-get update && \
    apt-get install -y vim wget build-essential git && \
    apt-get clean


# Install additional Python dependencies
RUN pip install --no-cache-dir streamlit pandas numpy pillow streamlit-autorefresh plotly TTS>=0.22.0

# Expose Streamlit default port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false", "--server.headless=true", "--server.fileWatcherType=auto"]