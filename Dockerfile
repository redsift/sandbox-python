FROM quay.io/redsift/sandbox:latest
MAINTAINER Christos Vontas email: christos@redsift.io version: 1.1.102

ENV PYTHONUNBUFFERED=1 PYTHONIOENCODING=UTF-8

LABEL io.redsift.sandbox.install="/usr/bin/redsift/install.py" io.redsift.sandbox.run="/usr/bin/redsift/run.py"

COPY root /

ARG v=3.10
ARG t=3

ENV version=${v} tag=${t}
ENV PYTHONPATH=$PYTHONPATH:$HOME/lib/python PATH=$PATH:$HOME/lib/python
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes
RUN apt-get update
RUN apt-get install -y build-essential curl git s3cmd python$version python$version-distutils python$version-dev
RUN curl -Ss https://bootstrap.pypa.io/get-pip.py | python$version
RUN curl -Ss https://bootstrap.pypa.io/get-pip.py | python$tag
RUN 

RUN chown -R root:root $HOME
RUN ln -fs /usr/bin/python3.10 /usr/bin/python3 && \
  apt-get purge -y && \
  rm -rf /root/.pip/cache/* /tmp/pip*

RUN python$version -m pip install --user -r /usr/bin/redsift/requirements.txt

RUN chown -R sandbox:sandbox $HOME

ENTRYPOINT ["/usr/bin/python"]
