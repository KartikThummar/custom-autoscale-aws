FROM ubuntu:latest
RUN apt update; apt install -y python3-numpy python3-distutils curl
RUN curl -fsSl "https://bootstrap.pypa.io/get-pip.py" > get_pip.py; python3 get_pip.py
RUN apt autoremove -y curl
RUN pip install pandas pymongo pytz
