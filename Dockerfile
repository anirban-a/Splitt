FROM python:3.10-slim
LABEL authors="anirban"

WORKDIR /app

COPY . /app


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV ENVIRONMENT=DEV

# Run uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]