# Use official Python image as base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY . /app/
RUN python manage.py collectstatic --noinput


# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "school_schedule.wsgi:application", "--bind", "0.0.0.0:8000"]
