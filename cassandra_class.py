from cassandra.cluster import Cluster

class Cassandra:
    def __init__(self):
        self.cluster = None
        self.session = None

    def connect_cassandra(self, host):
        self.cluster = Cluster([host])
        self.session = self.cluster.connect()

