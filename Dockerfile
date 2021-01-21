FROM ubuntu:18.04
LABEL mantainer='m.rysnik.42@gmail.com'

RUN \
       apt update \
    && apt upgrade -y \
    && apt install -y software-properties-common python3 python3-setuptools python3-pip \
    && add-apt-repository ppa:gijzelaar/snap7 \
    && apt update \
    && apt install -y libsnap7-dev libsnap7-1
ADD . /code
WORKDIR /code
COPY . .
# RUN python3 ./setup.py install
# RUN pip3 install python-snap7
RUN pip3 install -r requiremens.txt

EXPOSE 5000

CMD ["python3", "main.py"]
