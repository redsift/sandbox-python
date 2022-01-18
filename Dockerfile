FROM quay.io/redsift/sandbox:latest
MAINTAINER Christos Vontas email: christos@redsift.io version: 1.1.102

ENV PYTHONUNBUFFERED=1 PYTHONIOENCODING=UTF-8

LABEL io.redsift.sandbox.install="/usr/bin/redsift/install.py" io.redsift.sandbox.run="/usr/bin/redsift/run.py"

COPY root /

ARG v=3.10
ARG t=

ENV version=${v} tag=${t}
ENV PYTHONPATH=$PYTHONPATH:$HOME/lib/python PATH=$PATH:$HOME/lib/python

RUN export DEBIAN_FRONTEND=noninteractive && \
  apt-get update && \
  apt-get install -y \
  software-properties-common \
  build-essential git \
  s3cmd && \
  add-apt-repository ppa:deadsnakes/ppa && apt-get update && \
  apt-get install -y python$version python$version-dev python$version-distutils python$tag-pip && \
  chown -R root:root $HOME && \
  pip$tag install -U pip || true && \
  python$version -m pip install -U pip && \
  ln -fs /usr/bin/python3.10 /usr/bin/python3 && \
  apt-get purge -y && \
  rm -rf /root/.pip/cache/* /tmp/pip*

RUN python$version -m pip --version
RUN python$version -m pip install --user setuptools==59.5.0
RUN python$version -m pip install --user -r /usr/bin/redsift/requirements.txt

RUN chown -R sandbox:sandbox $HOME

ENTRYPOINT ["/usr/bin/python"]
