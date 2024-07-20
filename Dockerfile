# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install OS dependencies
RUN apt-get update && \
    apt-get install -y \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


# Copy the requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt


# Copy the rest of the application code to the container
COPY . /app/

RUN chmod +x /app/entrypoint.sh

# Expose the port the app runs on
EXPOSE 8000

CMD ["/app/entrypoint.sh"]