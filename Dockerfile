FROM python:3.8-slim

MAINTAINER Milan Das "milan.das77@gmail.com"
ENV APP_HOME /dockerapp
COPY ./app/ $APP_HOME/app/
COPY .env $APP_HOME
COPY client_secrets.json $APP_HOME
COPY requirements.txt $APP_HOME/
WORKDIR $APP_HOME
RUN pip install -r requirements.txt
ENV PYTHONPATH=$PYTHONPATH:$APP_HOME

ENTRYPOINT ["python"]
CMD ["app/gcp_oauth.py"]