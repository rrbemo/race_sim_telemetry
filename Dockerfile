FROM python:3.10-slim-buster

WORKDIR /race_sim_telemetry

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /race_sim_telemetry
EXPOSE 8080
CMD ["python", "app.py"]