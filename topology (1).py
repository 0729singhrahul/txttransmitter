from mininet.topo import Topo

class MyTopo( Topo ):
    def __init__( self ):

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        host1 = self.addHost( 'h1' )
        host2 = self.addHost( 'h2' )
        host3 = self.addHost( 'h3')
        Switch1 = self.addSwitch('s1')
        Switch2 = self.addSwitch('s2')
        # Add links
        self.addLink( host1, Switch1 )
        self.addLink( host2, Switch2 )
        self.addLink( host3, Switch2 )
        self.addLink( Switch1, Switch2 )

topos = { 'mytopo': ( lambda: MyTopo() ) }
