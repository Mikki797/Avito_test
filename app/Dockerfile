FROM python:3.8-slim

WORKDIR /src

COPY requirements.txt /src
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /src/app
ENV PYTHONPATH "${PYTHONPATH}:/src/app"

EXPOSE 8000

CMD python app/api.py