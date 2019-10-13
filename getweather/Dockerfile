FROM python:3-alpine

COPY . /getweather

WORKDIR /getweather

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

USER 5000

CMD ["python","app/getweather.py"]
