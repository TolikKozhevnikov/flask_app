FROM python:3.8-slim

ADD requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

ADD app.py /var/server/app.py

CMD python /var/server/app.py