FROM python:3

WORKDIR /app

RUN python3 -m venv env

COPY requirements.txt .

RUN ./env/bin/pip3 install --upgrade pip

RUN ./env/bin/pip3 install -r requirements.txt

VOLUME [ "/app/data" ]

EXPOSE 8080

COPY . .

RUN chmod +x ./execute.sh

CMD ["./execute.sh", "src/infrastructure/http/server.py"]