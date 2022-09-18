FROM python:latest

WORKDIR .

COPY ./* ./

RUN python3 -m pip install -U git+https://github.com/Rapptz/discord.py

RUN python3 -m pip install pillow requests

CMD ["python3", "bottom_meme.py", ""]
