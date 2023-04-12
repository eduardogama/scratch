FROM python:3.8-alpine


RUN apk add --update --no-cache \
        bash \
        tcpdump \
        iperf \
        busybox-extras \
        iproute2 \
        iputils
        
RUN pip3 install --upgrade pip

RUN adduser -D app
USER app
WORKDIR /app

ENV PATH="/app/.local/bin:${PATH}"
ENV PYTHONUNBUFFERED=1

COPY --chown=app:app . /app

RUN pip3 install -r requirements.txt



CMD [ "python", "app.py" ]
