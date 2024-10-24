FROM python:3.12.3-slim as builder

ADD requirements.txt /requirements.txt

RUN apt-get update -y -qq
RUN apt-get install -y --no-install-recommends ca-certificates make gcc g++ gdb strace unzip tcpdump curl git libssl-dev libxml2-dev \
    libbz2-dev libpq-dev libxslt-dev
RUN pip install virtualenv
RUN virtualenv --never-download /.venv
RUN /.venv/bin/python -m pip install --upgrade pip
RUN /.venv/bin/pip install -r /requirements.txt
RUN find /.venv/ -name __pycache__ | xargs rm -rf

# second stage
FROM python:3.12.3-slim

ARG APP_DIR=/app
ARG GIT_COMMIT=unspecified
ARG GIT_TAG=unspecified

WORKDIR ${APP_DIR}

COPY --from=builder /.venv /.venv
COPY --chown=root:root src/ /app/

# add back the dependencies
RUN set -x \
    && apt-get update -y -qq \
    && apt-get install -y --no-install-recommends vim jq git libpq-dev curl wget gettext-base \
    && apt clean  \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.cache \
    && find /app/ -name __pycache__ | xargs rm -rf

# environment
ENV PATH=/.venv/bin:/app:$PATH

CMD [ "python", "main.py"]
