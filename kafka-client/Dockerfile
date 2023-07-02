FROM python:3.8

RUN apt-get -qq update
RUN pip install --upgrade pip && pip install pip-tools
RUN apt-get install -y --no-install-recommends g++

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN source venv/bin/activate

# EXPOSE 7000
CMD python main.py
