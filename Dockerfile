FROM python:2

RUN apt-get update && \
    apt-get install -y libnanomsg-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY vendor /app/vendor
WORKDIR /app/vendor/nanomsg-python
RUN python setup.py install

COPY . /app
WORKDIR /app

LABEL io.redsift.dagger.init="install.py" io.redsift.dagger.run="bootstrap.py"
ENV SIFT_ROOT="/run/dagger/sift" \
	IPC_ROOT="/run/dagger/ipc" \
	PYTHONUNBUFFERED=1
# TODO: This doesn't work if sift root is overridden when running the
# container.
ENV PYTHONPATH="$SIFT_ROOT/server/site-packages"

ENTRYPOINT ["/usr/local/bin/python"]
