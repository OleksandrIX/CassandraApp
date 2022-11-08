gpg --keyserver keyserver.ubuntu.com --recv-keys 7E3E87CB

gpg --export --armor 7E3E87CB
sudo gpg --dearmour -o /etc/apt/trusted.gpg.d/cassandra-key.gpg

sudo sh -c 'echo "deb http://www.apache.org/dist/cassandra/debian 41x main" > /etc/apt/sources.list.d/cassandra.list'

sudo apt update

sudo apt install cassandra

sudo systemctl enable cassandra