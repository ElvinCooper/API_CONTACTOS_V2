FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


RUN chmod +X entrypoint.sh
ENV FLASK_APP=app.app


EXPOSE 8000
CMD [ "./entrypoint.sh"]


