FROM ubuntu:20.04
USER root
WORKDIR /app
COPY *.py /app/
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
    openvswitch-common \
    ifupdown \
    iproute2 \
    iptables \
    iputils-ping \
    net-tools \
    openvswitch-switch \
    openvswitch-testcontroller \
    python3-pip \
    mininet \
    sudo \
    curl
RUN pip install mininet
RUN touch /etc/network/interfaces 
RUN sudo service openvswitch-switch start


CMD ["sudo","python3", "main.py"]
