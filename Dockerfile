FROM python:3.10.13

WORKDIR .

COPY ./* ./

RUN python3 -m pip install discord.py

RUN python3 -m pip install -U git+https://github.com/edugomez102/twemoji-parser

RUN python3 -m pip install -r requirements.txt

CMD ["python3", "bottom_meme.py", ""]
