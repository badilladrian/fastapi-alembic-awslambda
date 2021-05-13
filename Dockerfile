FROM python:3.8.6-slim-buster

WORKDIR /usr/src/app

EXPOSE 8000

ENV PYTHONPATH=/usr/src/app

COPY  ./requirements.txt ./requirements.txt

RUN pip3 install --upgrade pip && pip3 install -r ./requirements.txt

COPY  ./scripts /usr/src/scripts

RUN chmod +x -R /usr/src/scripts

CMD ["/usr/src/scripts/init.sh"]
