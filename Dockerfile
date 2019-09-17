# Use oficial image of python 3
FROM python:3.7
# Add all files from the repository.
COPY . /PyQTT-Dashboard-API
# Set working directory to the one we've just copied.
WORKDIR /PyQTT-Dashboard-API
# Set environment variable for application
ARG APP_PORT
ENV APP_PORT=$APP_PORT
# Install dependencies.
RUN apt-get update
RUN apt-get install redis-server -y
RUN pip install -r requirements.txt
# Add the arguments we need to pass into the command above.
CMD ["sh", "-c", "service redis-server restart && python run.py"]