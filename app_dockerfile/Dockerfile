FROM python:3.9
EXPOSE 5000
ENV FLASK_ENV="development"
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY ../wsgi.py .
COPY ../app app
COPY ../logs.log .

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:5000", "wsgi:app"]
