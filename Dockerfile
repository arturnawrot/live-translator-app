FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

RUN chmod +x entrypoint.sh

RUN if [ ! -f .env ]; then cp .env.example .env; fi

# Google Cloud Run does not support command line, and all the environment variables
# must be added through their web interface. In such case we can get rid of the .env
# file because it's going to contain either empty or boilerplate values that will
# overwrite the variables set through Google Cloud Run and it will mess up the application.
# Set IS_RUNNING_ON_CLOUD variable through Google Cloud interface, not .env.
RUN if [ "$IS_RUNNING_ON_CLOUD" = "true" ]; then \
        rm -f .env; \
    fi

RUN apt-get update
RUN apt-get install -y ffmpeg

RUN pip install --upgrade pip && pip install -r src/requirements.txt

EXPOSE 80

WORKDIR /app/src

CMD ["/app/entrypoint.sh"]