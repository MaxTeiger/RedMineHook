FROM python:2.7

MAINTAINER Max Teiger <max.teiger@coopengo.com>

# install requirements

RUN pip install Flask==1.0.2
RUN pip install Flask-RESTful==0.3.7
RUN pip install jsonschema==2.6.0
RUN pip install python-redmine==2.2.1
RUN pip install requests==2.21.0
RUN pip install selenium==3.141.0
RUN pip install virtualenv==16.4.3
RUN pip install uwsgi
RUN pip install gevent
RUN pip install flask_api

ADD app.py /home/app.py
ADD redmine_api.py /home/redmine_api.py
#ADD config.py /home/config.py
ADD conf.txt /home/conf.txt

WORKDIR /home

CMD ["python", "app.py"]
