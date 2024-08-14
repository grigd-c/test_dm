FROM ubuntu:22.04
LABEL maintainer="Dmitriy Grigoryev <dgrigoryev@self>"

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
    build-essential \
    curl \
    ca-certificates \
    tcsh \
    gawk \
    vim \
    python3-dev \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install 'scanpy[leiden]'

USER root

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN mkdir /reporting
WORKDIR /reporting

# Copy everything into reporting
COPY ./ ./

WORKDIR /data
#CMD ["/bin/bash"]
