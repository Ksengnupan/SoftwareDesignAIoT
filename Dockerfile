#FROM node:14
#WORKDIR /app
#COPY package*.json ./
#RUN npm install
#COPY . .
#EXPOSE 3000
#CMD [ "node", "app.js" ]

FROM python:3.9-bullseye

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
#CMD ["python","-u","./app.py"] for blecollector
CMD ["python","-u","./app.py"] #for linebot
