import os
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time


def test_network_resilience(net):
    h1 = net.hosts[0]
    h2 = net.hosts[1]
    h3 = net.hosts[2]
    h4 = net.hosts[3]
    h5 = net.hosts[4]

    # Should pass
    info("Should pass\n")
    info(f"Testing h3 as master with IP {h3.IP()} and h1, h2, h3, h4, h5 as nodes\n")
    net.get('h3').cmd(f"python3 -m http.server 80 &") 
    for host in [h1, h2, h3, h4, h5]:
        result = host.cmd(f"curl -s -k http://{h3.IP()}")
        if "200 OK" in result:
            info(f"Connectivity to {host.name} from h3 is successful\n")
        else:
            info(f"Connectivity to {host.name} from h3 failed\n")

    # Configure loss between switches
    s1, s2 = net.get('s1'), net.get('s2')
    s1.config(loss=100)
    s2.config(loss=100)

    # Should fail
    info("Should fail\n")
    for host in [h1, h2, h3, h4, h5]:
        result = host.cmd(f"curl -s -k http://{h3.IP()}")
        if "200 OK" in result:
            info(f"Connectivity to {host.name} from h3 is successful after loss configuration\n")
        else:
            info(f"Connectivity to {host.name} from h3 failed after loss configuration\n")

    # Reset loss configuration
    s1.config(loss=0)
    s2.config(loss=0)


def setup_topology():
    floodlight_ip = "172.18.0.2"
    floodlight_port = 6653

    net = Mininet(controller=RemoteController)
    print(f"Starting Mininet with IP: {floodlight_ip} and port: {floodlight_port}")
    time.sleep(1)
    net.addController(
        controller=RemoteController,
        switch=OVSSwitch,
        link=TCLink,
        ip=floodlight_ip,
        port=floodlight_port,
        waitConnected=True,
    )
    s1 = net.addSwitch("s1")
    s2 = net.addSwitch("s2")
    h1 = net.addHost("h1")
    h2 = net.addHost("h2")
    h3 = net.addHost("h3")
    h4 = net.addHost("h4")
    h5 = net.addHost("h5")

    net.addLink(h1, s1, port1=1)
    net.addLink(h2, s1, port1=2)
    net.addLink(h3, s1, port1=3)
    net.addLink(h3, s2, port1=1)
    net.addLink(h4, s2, port1=2)
    net.addLink(h5, s2, port1=3)
    s1.cmd("ifconfig s1-tap0 10.0.10.1 netmask 255.255.255.0")
    s2.cmd("ifconfig s2-tap1 10.0.20.1 netmask 255.255.255.0")
    net.start()

    # Test
    test_network_resilience(net)

    # Start CLI
    CLI(net)

    # Stop network
    net.stop()



if __name__ == "__main__":
    setLogLevel("info")
    setup_topology()
