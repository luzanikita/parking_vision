FROM python:3.6

ENV FLASK_APP run.py

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY run.py gunicorn-cfg.py requirements.txt config.py .env ./

COPY app app

CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
