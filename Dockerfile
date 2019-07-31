FROM python:alpine
RUN apk --no-cache add build-base python-dev py-pip jpeg-dev zlib-dev git
RUN pip install --no-cache-dir discord requests
RUN pip install --no-cache-dir git+https://github.com/python-pillow/Pillow.git@6459cafba365271a5ad0666f0c097662165e2240
ADD *.py /runescape/
ADD runescape_uf.ttf /runescape/
WORKDIR /runescape/
CMD python /runescape/runescapeBot.py
