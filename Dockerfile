FROM quay.io/redsift/sandbox:22.04-beta
MAINTAINER Christos Vontas email: christos@redsift.io version: 1.1.102

ENV PYTHONUNBUFFERED=1 PYTHONIOENCODING=UTF-8

LABEL io.redsift.sandbox.install="/usr/bin/redsift/install.py" io.redsift.sandbox.run="/usr/bin/redsift/run.py"

COPY root /

ARG v=3.11
ARG t=3

ENV version=${v} tag=${t}
ENV PYTHONPATH=$PYTHONPATH:$HOME/lib/python PATH=$PATH:$HOME/lib/python
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes
RUN curl https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | apt-key add -
RUN echo 'deb https://apt.kitware.com/ubuntu/ jammy main' > /etc/apt/sources.list.d/cmake.list
RUN apt update
RUN apt install -y build-essential cmake git s3cmd
RUN apt install -y python$version python$version-dev python$version-venv python$version-distutils
RUN python$version -m ensurepip --upgrade

RUN chown -R root:root $HOME
RUN ln -fs /usr/bin/python3.11 /usr/bin/python3 && \
  apt purge -y && \
  rm -rf /root/.pip/cache/* /tmp/pip*

RUN python$version -m pip install --user -r /usr/bin/redsift/requirements.txt

RUN chown -R sandbox:sandbox $HOME

ENTRYPOINT ["/usr/bin/python"]
