FROM jenkins/jenkins:lts
USER root
RUN apt-get update \
&& apt-get install -y python-pip python3 \
&& rm -rf /var/lib/apt/lists/*
RUN pip install tox
