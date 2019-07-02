FROM python:3.6-jessie
RUN pip install discord requests
RUN pip install git+https://github.com/python-pillow/Pillow.git@6459cafba365271a5ad0666f0c097662165e2240
ADD *.py /runescape/
ADD runescape_uf.ttf /runescape/
WORKDIR /runescape/
CMD python /runescape/runescapeBot.py