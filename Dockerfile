FROM python:3.8
RUN apt-get update -y
# Set the working directory to /app
# If the WORKDIR doesn’t exist, it will be created even if it’s not used in any subsequent Dockerfile instruction.
WORKDIR /app
# Copy the current directory contents into the container at /app
COPY . /app
RUN python -m pip install -U pip
RUN pip install -r requirements.txt