# Use oficial image of python 3
FROM python:3.7
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1
# Add all files from the repository.
COPY . /PyQTT-Dashboard-API
# Set working directory to the one we've just copied.
WORKDIR /PyQTT-Dashboard-API
# Export port for the application
EXPOSE $APP_PORT
# Install dependencies.
RUN pip install -r requirements.txt
# Create the database and start the server.
CMD ["sh", "-c", "python manage.py db create && python manage.py runserver"]