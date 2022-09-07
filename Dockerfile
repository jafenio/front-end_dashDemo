FROM python:3.10.5

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install -r requirements.txt

ENV BACKEND_URL=http://172.17.0.2:5000/msdemo/v1

EXPOSE 3000

CMD [ "python3","app.py"]