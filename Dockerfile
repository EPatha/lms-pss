FROM python:3.11

# Set working directory
WORKDIR /code

# Copy requirements and install dependencies
COPY code/requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY code/ /code/

# Expose port 8000 (optional, for documentation)
EXPOSE 8000

# Default command (can be overridden by docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
