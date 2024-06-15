# Use the official Spark image from Apache Spark
FROM bitnami/spark:latest

# Install Delta Lake dependencies
RUN pip install delta-spark

# Set the working directory
WORKDIR /app

# Copy your Spark application into the container
COPY etl.py .

# Set environment variables for Spark
ENV SPARK_HOME=/opt/bitnami/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Define the command to run your Spark application
CMD ["spark-submit", "--packages", "io.delta:delta-core_2.12:1.0.0", "/app/etl.py"]
