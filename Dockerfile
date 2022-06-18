FROM python:3.9
EXPOSE 5000
ENV FLASK_ENV="development"
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
COPY ./wsgi.py .
COPY ./app app
COPY ./logs.log .

ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]
