import subprocess
import os
from cassandra.cluster import Cluster
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# result = session.execute("select * from system_schema. where keyspace_name = 'test'")
#
# for i in result:
#     print(i)
# session.execute("create table users (name text, age int)")
# session.execute("insert into test.users (name, age) values ('sasha', 19)")
# res = session.execute("select * from system_schema.columns where keyspace_name = 'test' and table_name = 'users'")
# arr = []
# for i in res:
#     arr.append(i.column_name)
# arr.reverse()
# print(arr)
keyspace = 'sasha'
session.execute("create keyspace {} with replication = {'class': 'SimpleStrategy', 'replication_factor' : 1}" % keyspace)
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
