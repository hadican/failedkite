FROM python:3.11-alpine

WORKDIR /app

VOLUME /config/author_mapping.yml

RUN pip install --no-cache-dir Flask==2.3.2 slackclient==2.9.4 gunicorn==21.2.0 PyYAML==6.0.1

COPY *.py /app/

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]