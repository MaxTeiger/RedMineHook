FROM python:2.7

MAINTAINER Max Teiger <max.teiger@coopengo.com>

# install requirements

RUN pip install --upgrade "Flask==1.0.2" \
    "Flask-RESTful==0.3.7" \
    "jsonschema==2.6.0" \
    "python-redmine==2.2.1" \
    "requests==2.21.0" \
    "uwsgi" \
    "gevent" \
    "flask_api" 

ADD app.py /home/app.py
ADD redmine_api.py /home/redmine_api.py

RUN cd /home && touch conf.txt

CMD ["python", "home/app.py"]
