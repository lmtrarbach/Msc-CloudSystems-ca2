from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI


class CloudVPCTopo(Topo):
    def build(self):
        # Define switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        # Define hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        # Add links
        self.addLink(h1, s1)
        self.addLink(s1, s2)
        self.addLink(s2, h2)

def create_network():
    topo = CloudVPCTopo()
    net = Mininet(topo)
    net.start()
    CLI(net)  # This allows you to interact with the network in the Mininet CLI
    net.stop()

if __name__ == '__main__':
    create_network()
