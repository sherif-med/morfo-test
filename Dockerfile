FROM python:3.11-slim

# Install uv
RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh

# Set workdir
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies using uv
RUN uv install

CMD ["uv", "run", "main.py"]