FROM tiangolo/uwsgi-nginx-flask:python3.8

# Install the requirements first since they're less likely to change, and so can be cached better.
COPY /requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# More likely to change
COPY /app/ /app/
COPY /crex/ /app/crex/
COPY /data/ /app/data/

ENV LISTEN_PORT 5000
EXPOSE 5000
