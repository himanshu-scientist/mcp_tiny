FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies (adjust if you use a requirements.txt or similar)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your server will listen on
EXPOSE 8000

# Default command
CMD ["fastmcp", "run", "server.py", "--transport", "http", "--host", "0.0.0.0"]