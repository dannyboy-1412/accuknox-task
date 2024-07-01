# Use an official Python runtime as our base image
FROM python:3.12-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages, such as this Django project's dependencies
RUN pip install -r requirements.txt

# Expose the port that our container will use
EXPOSE 8000

# Run the command to start the Django development server on container startup
CMD ["python", "src/social_network/manage.py", "runserver", "0.0.0.0:8000"]
