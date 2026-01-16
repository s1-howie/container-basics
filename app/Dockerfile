# 1. Base Image: Start with a lightweight Python image
FROM python:3.11-slim

# 2. Workdir: Set the working directory inside the container
WORKDIR /app

# 3. Dependencies: Copy requirements first to leverage Docker Layer Caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy Code: Copy the rest of the application code
COPY . .

# 5. Environment: Set default environment variables (can be overridden at runtime)
ENV APP_PORT=5000
ENV APP_MESSAGE="Default Message"

# 6. Expose: Document that this container listens on port 5000
EXPOSE 5000

# 7. Command: The command to run when the container starts
CMD ["python", "main.py"]
