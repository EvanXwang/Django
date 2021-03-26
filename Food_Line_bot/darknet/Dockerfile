FROM ubuntu:18.04

WORKDIR /var/app

COPY . .

RUN apt-get update && apt-get install -y unzip python3-pip joe libsm6 libxext6 libxrender-dev

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

RUN make clean && make

CMD ["python3", "./FoodLine/manage.py", "runserver", "0.0.0.0:8000", "--noreload"]