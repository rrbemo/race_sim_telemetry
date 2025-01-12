FROM python:3.13-alpine

WORKDIR /race_sim_telemetry

RUN apk update

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .
EXPOSE 8080
CMD ["python", "app.py"]