import os
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time


def test_network_resilience(net):
    info("Testing - Should all pass\n")
    # Testing with all working setup
    for each in range(1, 6):
        if each != 4:
            to_host = net.get("host{each}")
            result = net.get("host{each}").cmd(f"ping -c 2 host4")
            if " 0% packet loss" in result:
                info(f"Connectivity between host4 and host{each} is successful")
            else:
                info(f"Connectivity between host4 and host{each} failed")

    net.get("host4").cmd("iptables -A INPUT -j DROP")

    info("Testing - Should fail")
    for each in range(1, 6):
        if each != 4:
            to_host = net.get("host{each}")
            result = net.get("host{each}").cmd(f"ping -c 2 host4")
            if " 0% packet loss" in result:
                info(f"Connectivity between host4 and host{each} is successful")
            else:
                info(f"Connectivity between host4 and host{each} failed")

    # Reset iptables rules
    net.get("host4").cmd("iptables -D OUTPUT -s 10.0.0.1 -d 10.0.0.2 -j DROP")
    net.get("host2").cmd("iptables -D OUTPUT -s 10.0.0.2 -d 10.0.0.1 -j DROP")

    # Reset connectivity
    info("Testing - Should all pass again")
    net.pingAll()


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
    host1 = net.addHost("host1")
    host2 = net.addHost("host2")
    host3 = net.addHost("host3")
    host4 = net.addHost("host4")
    host5 = net.addHost("host5")

    net.addLink(host1, s1)
    net.addLink(host2, s1)
    net.addLink(host3, s2)
    net.addLink(host4, s1)
    net.addLink(host4, s2)
    net.addLink(host5, s2)

    net.start()

    # Connect host4 directly to both switches
    net.addLink(host4, s1)
    net.addLink(host4, s2)

    # Test
    test_network_resilience(net)

    # Start CLI
    CLI(net)

    # Stop network
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    setup_topology()
