FROM python:3.5.5
ADD . /code
WORKDIR /code
RUN pip install -r requirements_server.txt
CMD ["bash", "start.sh"]
