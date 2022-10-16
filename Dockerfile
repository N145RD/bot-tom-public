FROM python:latest

WORKDIR .

COPY ./* ./

RUN python3 -m pip install -U git+https://github.com/Rapptz/discord.py

RUN python3 -m pip install -U git+https://github.com/edugomez102/twemoji-parser

## RUN python3 -m pip install pillow requests emoji==1.7

RUN python3 -m pip install -r requirements.txt

CMD ["python3", "bottom_meme.py", ""]
