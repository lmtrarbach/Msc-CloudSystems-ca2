import os
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time

def setup_topology():
    floodlight_ip = "172.18.0.2"
    floodlight_port = 6653

    net = Mininet(controller=RemoteController)
    print(f'Starting mininet with IP: {floodlight_ip} and port: {floodlight_port}')
    time.sleep(1)
    net.addController(controller=RemoteController,switch=OVSSwitch, link=TCLink, ip=floodlight_ip, port=floodlight_port, waitConnected=True)
    s1 = net.addSwitch('s1')
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')

    net.addLink(h1, s1)
    net.addLink(h2, s1)

    net.start()

    # Test 
    info("Testing connectivity...\n")
    net.pingAll()

    # Interact with Floodlight
    info("\n\nInteracting with Floodlight controller...\n")
    print(s1)


    # Start CLI
    CLI(net)

    # Stop network
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    setup_topology()
