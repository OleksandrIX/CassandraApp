from cassandra.cluster import Cluster

class Cassandra:
    def __init__(self):
        self.cluster = None
        self.session = None

    def connect_cassandra(self, host):
        self.cluster = Cluster([host])
        self.session = self.cluster.connect()

    def get_all_keyspace(self):
        result = self.session.execute("select * from system_schema.keyspaces")
        keyspaces = []
        for i in result:
            keyspaces.append(i.keyspace_name)
        return keyspaces

    def get_all_tables_of_keyspace(self, keyspace):
        result = self.session.execute(f"select * from system_schema.tables where keyspace_name = '{keyspace}'")
        tables_of_keyspace = []
        for i in result:
            tables_of_keyspace.append(i.table_name)
        return tables_of_keyspace

    def get_all_column_of_table(self, keyspace, table):
        result = self.session.execute(f"select * from system_schema.columns where keyspace_name = '{keyspace}' and table_name = '{table}'")
        column_of_table = []
        for i in result:
            column_of_table.append(i.column_name)
        column_of_table.reverse()
        return column_of_table

    def get_info_of_column(self, keyspace, table):
        result = self.session.execute(f"select * from {keyspace}.{table}")
        info_of_columns = []
        for i in result:
            info_of_columns.append(list(i))
        return info_of_columns

    def add_keyspace(self, keyspace):
        self.session.execute(f"create keyspace {keyspace} with replication = {'class': 'SimpleStrategy', 'replication_factor' : 1}")
