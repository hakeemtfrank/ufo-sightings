FROM python:3.6-stretch

RUN apt-get update && \
	apt-get install -y gcc wget python3-pip python3-dev && \
	pip3 install --upgrade pip

WORKDIR  /usr/src/ufo-sightings

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /src/
RUN ls -la /src/* && \
	bash /data/get_data.sh

CMD ["python3", "/src/main.py", "-i data/scrubbed.csv", "-o data/ufo_sightings.csv"]

LABEL maintainer="Hakeem Frank"