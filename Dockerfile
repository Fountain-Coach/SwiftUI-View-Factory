FROM swift:5.10-jammy

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first for caching
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

ENTRYPOINT ["python3", "cli/vi.py"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
