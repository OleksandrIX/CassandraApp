import customtkinter
from desktop_class import CTkApp

app = CTkApp('CassandraApp')

app.verify_cassandra()

app.start()
