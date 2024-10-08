# Use the Python 3.10 Alpine base image
FROM python:3.10-alpine

# Set the working directory
WORKDIR /code

# Set environment variables for Flask
ENV FLASK_APP=routes.py
ENV FLASK_RUN_HOST=0.0.0.0

# Install necessary packages
RUN apk add --no-cache gcc musl-dev linux-headers

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 5000

# Copy the application code
COPY ./customer-api .

# Command to run the Flask application
CMD ["flask", "run", "--debug"]
