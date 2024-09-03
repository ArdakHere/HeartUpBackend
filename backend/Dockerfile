FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /HeartUpBackend

# Install dependencies
COPY requirements.txt /HeartUpBackend/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /HeartUpBackend/
RUN python manage.py collectstatic --noinput
VOLUME /HeartUpBackend/media

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]