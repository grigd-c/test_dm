FROM gcfntnu/scanpy:1.9.1
MAINTAINER Dmitriy Grigoryev <dgrigoryev@self>

USER root

RUN mkdir /reporting
WORKDIR /reporting

# Copy everything into reporting
COPY ./ ./

WORKDIR /data
#CMD ["/bin/bash"]
