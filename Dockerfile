FROM python:3.9-slim

WORKDIR /app

# install camels_datasetloader from github
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/CAMELS-DE/camels_datasetloader.git
RUN pip install -e camels_datasetloader

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]