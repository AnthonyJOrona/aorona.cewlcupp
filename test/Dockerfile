FROM python:3.10.4-bullseye

RUN pip install pexpect
RUN apt-get update \
    && apt-get install -y cupp=0.0+20190501.git986658-6 \
    && apt-get install -y cewl=5.4.9-2

WORKDIR /usr/local/bin
COPY cewlcupp.py .

CMD ["python", "cewlcupp.py"]