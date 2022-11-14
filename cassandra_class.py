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
        result = self.session.execute(
            f"select * from system_schema.columns where keyspace_name = '{keyspace}' and table_name = '{table}'")
        columns = {}
        for i in result:
            columns[i.column_name] = i.type
        return columns

    def get_pk_of_table(self, keyspace, table):
        result = self.session.execute(
            f"select * from system_schema.columns where keyspace_name = '{keyspace}' and table_name = '{table}'")
        pk_name = ''
        for i in result:
            if i.kind == 'partition_key':
                pk_name = i.column_name
        return pk_name

    def get_all_pk_value(self, keyspace, table, pk_key):
        result = self.session.execute(f"select {pk_key} from {keyspace}.{table}")
        pk_values = []
        for i in result:
            pk_values.append(list(i)[0])
        return pk_values

    def get_info_of_column(self, keyspace, table):
        result = self.session.execute(f"select * from {keyspace}.{table}")
        info_of_columns = []
        for i in result:
            info_of_columns.append(list(i))
        return info_of_columns

    def get_name_column_of_text(self, keyspace, table):
        result = self.session.execute(f"select * from system_schema.columns WHERE keyspace_name='{keyspace}' and table_name = '{table}'")
        keys = []
        for i in result:
            if i.type == 'text':
                keys.append(i.column_name)
        keys.reverse()
        return keys

    def add_keyspace(self, keyspace):
        self.session.execute(
            "create keyspace " + keyspace + " with replication = {'class': 'SimpleStrategy', 'replication_factor' : 1}")

    def drop_keyspace(self, keyspace):
        self.session.execute(f"drop keyspace {keyspace}")

    def add_table_in_keyspace(self, keyspace, table, key_values, pk):
        self.session.execute(f"create table {keyspace}.{table} ({key_values}PRIMARY KEY({pk}))")

    def drop_table_in_keyspace(self, keyspace, table):
        self.session.execute(f"drop table {keyspace}.{table}")

    def add_row_in_table(self, keyspace, table, columns_name, columns_value):
        self.session.execute(f"insert into {keyspace}.{table} ({columns_name}) values ({columns_value})")

    def drop_row_in_table(self, keyspace, table, pk_key, pk_value):
        self.session.execute(f"delete from {keyspace}.{table} where {pk_key} = '{pk_value}'")
