# My_Dashboard

This repository generates Docker images for an interactive dashboard built using the Streamlit library. The instructions below guide you through setting up, building, and deploying the Docker container for the Streamlit dashboard.
<img width="632" alt="image" src="https://github.com/user-attachments/assets/c5cb9bbc-bc60-4d4e-8fa3-87fe6f183ca4">

---------------------------------------------------------------------------------------------------------

# Setting Up Docker

1. Create a Directory for Docker Files
   
  mkdir my-container
  cd my-container

2. Write a Dockerfile
   
  Create a Dockerfile and include necessary system-level installations like vim and other dependencies using apt install.
  Install Python dependencies by specifying them in a requirements.txt file.
  Set up file watchers for detecting changes in your local data (if needed).
  Example of a basic Dockerfile:

---------------------------------------------------------------------------------------------------------

# Command to run the Streamlit app

1. Build and Run Docker Images

  Build Docker Image
  
  docker build -t streamlit-dashboard .
  For Apple M1/M2 (ARM64) or cross-platform compatibility:
  
  docker build --platform linux/amd64 -t streamlit-dashboard .
  Run Docker Container
  
  docker run -p 8501:8501 -v $(pwd):/app streamlit-dashboard
  For cross-platform compatibility:
  
  docker run --platform linux/amd64 -p 8501:8501 -v $(pwd):/app streamlit-dashboard
  Deploying Docker

2. Create a Docker Image File

  Save your running container as a Docker image:
  docker commit <container_id> <image_name>
  Export the image to a .tar file:

   docker save -o <path_to_save>/image.tar <image_name>

3. Transfer Docker Image to Another Server

  Move the Docker image file to an offline or remote server:
  scp ./image.tar <username>@<offline_server_ip>:<destination_path>

4. Load Docker Image on the Target Server

  On the target server, load the Docker image:
  docker load -i <path_to_image>/image.tar

5. Run Docker Container

  Start the Docker container using the loaded image:
  docker run -p 8501:8501 -v $(pwd):/app streamlit-dashboard

---------------------------------------------------------------------------------------------------------

Notes

- When building for ARM64 (e.g., Apple M1/M2 chips), consider compatibility by specifying --platform linux/amd64.
- Ensure requirements.txt includes all necessary Python libraries for your Streamlit application.
- Use volume mounting (-v $(pwd):/app) to keep local files synchronized with the container during development.
