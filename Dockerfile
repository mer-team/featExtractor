FROM python:2.7-slim-buster

ARG HOST=localhost
ARG USER=guest
ARG PASS=guest
ARG PORT=5672
ARG MNG_PORT=15672
ARG TIME=10

COPY /src /featExtractor

WORKDIR /featExtractor

RUN apt-get update && apt-get install curl -y
RUN rm -rf /var/lib/apt/lists

RUN pip install -r ./requirements.txt

RUN chmod +x ./wait-for-rabbit.sh

CMD ["./wait-for-rabbit.sh", "python", "featuresExtraction.py"]