FROM python:3.8
WORKDIR /app
COPY ./requirements.txt . 
RUN pip install -r requirements.txt
COPY . .
EXPOSE $PORT
CMD uvicorn app:app --host "0.0.0.0" --port $PORT
