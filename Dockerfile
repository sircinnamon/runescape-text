FROM python:3.6-jessie
RUN pip install discord requests pillow
ADD *.py /runescape/
ADD runescape_uf.ttf /runescape/
WORKDIR /runescape/
COPY scpillow/src/PIL/GifImagePlugin.py /usr/local/lib/python3.6/site-packages/PIL/
CMD python /runescape/runescapeBot.py