FROM quay.io/redsift/sandbox:latest
MAINTAINER Christos Vontas email: christos@redsift.io version: 1.1.102

ENV PYTHONUNBUFFERED=1 PYTHONIOENCODING=UTF-8

LABEL io.redsift.sandbox.install="/usr/bin/redsift/install.py" io.redsift.sandbox.run="/usr/bin/redsift/run.py"

COPY root /

ARG v=3.8
ARG t=

ENV version=${v} tag=${t}
ENV PYTHONPATH=$PYTHONPATH:$HOME/lib/python
ENV PATH=$PATH:$HOME/lib/python

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y software-properties-common \
                       build-essential \
                       libicu-dev \
                       git \
                       s3cmd
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python$version \
                       python$version-dev \
                       python$version-distutils \
                       python$version-venv \
                       python$tag-pip

RUN chown -R root:root $HOME
RUN pip$tag install -U pip || true
RUN python$version -m pip install -U pip
RUN ln -fs /usr/bin/python$version /usr/bin/python3
RUN apt-get purge -y && rm -rf /root/.pip/cache/* /tmp/pip*

RUN python$version -m pip --version
RUN python$version -m pip install --user setuptools==51.1.1
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python$version -

# Setup virtual env for all the libraries
ENV VIRTUAL_ENV="$HOME/venv"
RUN python$version -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$HOME/.poetry/bin:$PATH"

RUN python -m pip install -r /usr/bin/redsift/requirements.txt

RUN chown -R sandbox:sandbox $HOME

ENTRYPOINT ["python"]
