# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --timeout=1000 -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . .

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable
ENV STREAMLIT_SERVER_PORT 8501
ENV STREAMLIT_SERVER_ADDRESS 0.0.0.0

# Run app.py when the container launches
CMD ["streamlit", "run", "ui/app.py"]
