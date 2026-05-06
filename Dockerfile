# ------------------------------------------------------------------------------------------
# 1. Use an official lightweight Python image as the base
#   'python:3.11-slim' is a small, optimized image with Python 3.11 preinstalled
# ------------------------------------------------------------------------------------------
FROM python:3.11-slim

# ------------------------------------------------------------------------------------------
# 2. Install system dependencies (to be installed in container's PC) required by psycopg2 and Django
# ------------------------------------------------------------------------------------------
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       libc-dev \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------------------------------
# 3. Set environment variables
# ------------------------------------------------------------------------------------------
#   Prevents Python from writing .pyc files and __pycache__ directories
#   This keeps the container filesystem clean and avoids unnecessary writes
ENV PYTHONDONTWRITEBYTECODE=1

#   Ensures that Python output is sent straight to the terminal (stdout/stderr)
#   without being buffered, so logs appear immediately (helpful for debugging in Docker)
ENV PYTHONUNBUFFERED=1

ENV DJANGO_SETTINGS_MODULE=projectmanagement.settings

# ------------------------------------------------------------------------------------------
# 4. Set the working directory inside the container
#   Creates the directory '/projectmanagement' if it doesn't exist
#   and sets it as the default directory for all subsequent commands (RUN, COPY, CMD, etc.)
# ------------------------------------------------------------------------------------------
WORKDIR /projectmanagement

# ------------------------------------------------------------------------------------------
# 5. Copy only requirements.txt into the container
#   This is done separately before copying all source code to take advantage of Docker’s caching
# ------------------------------------------------------------------------------------------
COPY requirements.txt ./

# ------------------------------------------------------------------------------------------
# 6. Install Python dependencies inside the container
#   Uses pip to install all packages listed in requirements.txt
#   '--no-cache-dir' can be added to reduce image size by skipping pip’s cache
# ------------------------------------------------------------------------------------------
RUN pip install -r requirements.txt

# ------------------------------------------------------------------------------------------
# 7. Copy the rest of the application code into the container
#   This copies all files from your project folder on the host machine
#   into the '/projectmanagement' directory inside the container
# ------------------------------------------------------------------------------------------
COPY . .

# ------------------------------------------------------------------------------------------
# 8. Expose port 8000 to the outside world
#   This tells Docker (and users) that the application inside the container
#   will listen on port 8000 (common for Django apps)
# ------------------------------------------------------------------------------------------
EXPOSE 8000

# ------------------------------------------------------------------------------------------
# 9. Define the default command to run INSIDE THE CONTAINER when the container starts
#   Here, it starts Django’s development server, binding it to 0.0.0.0:8000
#   Without 0.0.0.0, Django would default to 127.0.0.1 (localhost), which would not be reachable from outside the container.
#   so it can accept external connections (not just from inside the container)

#   ************ Why we put CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] *************
#   Because when the container starts, it needs something to run.
#   If you don’t give CMD, Docker will ask: “What should I run inside this container?”.
#   So people usually put runserver there, so Django starts automatically when you do:
#   ----> docker compose -f file_name.yaml up -d
# ------------------------------------------------------------------------------------------
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


