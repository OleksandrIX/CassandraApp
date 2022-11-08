import subprocess
import os

#
# cmd = subprocess.Popen(['echo', 'h6ejtsPW'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
# subprocess.run(['sudo', '-S', 'sh', 'script_install_cassandra.sh'], stdin=cmd.stdin)

password = 'h6ejtsPW'
command = 'apt install git -y'
command_install_cassandra = 'sh script_install_cassandra.sh'
command_install_jdk = 'sh script_install_jdk.sh'

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


p = os.system('echo %s|sudo -S %s' % (password, command))
print(f'{p}!!!!!!!')
