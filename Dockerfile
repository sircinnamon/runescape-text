FROM python:3.13-alpine
RUN apk add --no-cache jpeg-dev zlib-dev
RUN MULTIDICT_NO_EXTENSIONS=1 YARL_NO_EXTENSIONS=1 pip install --no-cache-dir Pillow
RUN mkdir /python
WORKDIR /python
