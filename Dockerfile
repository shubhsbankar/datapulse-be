# Use a Python base image
FROM python:3.10

# Install Poetry
RUN pip install poetry

# Set the working directory
WORKDIR /app

# Copy pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock /app/

# Install dependencies using Poetry
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application
COPY . /app/

# Command to run the app
CMD ["poetry", "run", "python", "main.py"]
