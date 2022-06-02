FROM node:17.0.0-bullseye AS build_webapp

WORKDIR /output

COPY ./webapp .

RUN npm install

RUN npm run build


FROM python:3 AS runtime

WORKDIR /app

RUN python3 -m venv env

COPY requirements.txt .

RUN ./env/bin/pip3 install --upgrade pip

RUN ./env/bin/pip3 install -r requirements.txt

VOLUME [ "/app/data" ]

EXPOSE 8080

COPY . .

COPY --from=build_webapp ./output/dist /app/webapp/dist

RUN chmod +x ./execute.sh

CMD ["./execute.sh", "src/server.py"]