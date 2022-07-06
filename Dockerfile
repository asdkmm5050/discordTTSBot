FROM python:3.8

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

COPY ./audio.py /app/
COPY ./bot.py /app/
COPY ./config.json /app/
WORKDIR /app
RUN pip install discord
RUN pip install discord-py-slash-command==3.0.3
RUN pip install gTTs
RUN pip install ffmpeg
RUN pip install PyNaCl
CMD python ./bot.py