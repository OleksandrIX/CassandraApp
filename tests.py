import subprocess
import os
import inspect
from cassandra.cluster import Cluster
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# result = session.execute("select * from system_schema. where keyspace_name = 'test'")
#
# for i in result:
#     print(i)
# session.execute("create table users (name text, age int)")
# name = "'dima', 20"
# age = 20
# session.execute(f"insert into test.users (name, age) values ({name})")
# res = session.execute("select * from system_schema.columns WHERE keyspace_name='test' and table_name = 'users'")

# for i in res:
#     print(i.type, i.column_name)
# arr = []
# for i in res:
#     if i.kind == 'partition_key':
#         print(i.column_name)


# keyspace = 'sasha'
# session.execute("create keyspace " + keyspace + " with replication = {'class': 'SimpleStrategy', 'replication_factor' : 1}")
# res = session.execute("select * from system_schema.columns where keyspace_name = 'dimon' and table_name = 'dimooon'")

class Add:
    def __init__(self):
        self.a = 10
        self.b = 20


def props(obj):
    pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and not inspect.ismethod(value):
            pr[name] = value
    return pr


result = session.execute("select * from system_schema.columns where keyspace_name = 'dimon' and table_name ='dimooon'")
row_keys = []
row = {}
for i in result:
    row[i.column_name] = i.type
    row_keys.append(row)
    row = {}
print(row_keys)

res = session.execute("select * from dimon.dimooon")
rows = []
row = {}
for i in res.:

    temp = props(i)
    keys = list(temp['_fields'])
    # print(temp)
    for j in range(len(keys)):
        print(keys[j])
        print(row_keys[keys[j]])
        print(temp[keys[j]])
        rows.append([keys[j], row_keys[keys[j]], temp[keys[j]]])
# print(rows)
# print(r[0]['_fields'])

# res = session.execute("select * from test.users")
# arr=[]
# for i in res:
#     arr.append(list(i))
#
# for i in range(len(arr)):
#     print(type(arr[i]))
#
# cmd = subprocess.Popen(['echo', 'h6ejtsPW'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
# subprocess.run(['sudo', '-S', 'sh', 'script_install_cassandra.sh'], stdin=cmd.stdin)

# password = 'h6ejtsPW'
# command = 'apt install git -y'
# command_install_cassandra = 'sh script_install_cassandra.sh'
# command_install_jdk = 'sh script_install_jdk.sh'

# p = os.system('which cassandra')
# print(f'{p} !')

# if os.system('which java') != 0:
#     os.system('echo %s|sudo -S %s' % (password, command_install_jdk))
#     if os.system('which cassandra') != 0:
#         os.system('echo %s|sudo -S %s' % (password, command_install_cassandra))
#         print('CASSANDRA INSTALLED!!!')
#     else:
#         print('CASSANDRA ALREADY INSTALLED!!!')
# elif os.system('which cassandra') != 0:
#     print('JAVA ALREADY INSTALLED!!!')
#     os.system('echo %s|sudo -S %s' % (password, command_install_cassandra))
#     print('CASSANDRA INSTALLED!!!')
# else:
#     print('JAVA AND CASSANDRA ALREADY INSTALLED!!!')

#
# p = os.system('echo %s|sudo -S %s' % (password, command))
# print(f'{p}!!!!!!!')
