from mininet.topo import Topo
class DC6GTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1')
        self.addLink(h1, s1, bw=100, delay='1ms')

topos = {'dc6g': DC6GTopo}
