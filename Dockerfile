# Use a base image
FROM intel/intel-optimized-pytorch

# Set the working directory
WORKDIR /app

# Install any dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the main.py file and related folders
COPY .env /app/.env
COPY main.py /app/
COPY src /app/src
COPY data /app/data
COPY model_weights /app/model_weights
COPY model.properties /app/model.properties

# Set the entrypoint command
CMD ["tail", "-f", "/dev/null"]
