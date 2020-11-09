FROM python:3.8-slim-buster
WORKDIR /
ADD . /project
RUN pip install -r requirements.txt
CMD ["python","main.py"]