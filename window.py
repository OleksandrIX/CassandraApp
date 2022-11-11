import customtkinter
from tkinter import *


class Window:
    def __init__(self, parent, width, height):
        self.app = customtkinter.CTkToplevel(parent)
        self.center_window(width, height)
        self.lable = customtkinter.CTkLabel(self.app)
        self.entry = customtkinter.CTkEntry(self.app)
        self.button = customtkinter.CTkButton(self.app)
        self.cb = customtkinter.CTkComboBox(self.app)
        self.cassandra_cluster = None
        self.y_widget = 0.3
        self.widgets_to_add_table = []
        self.button_add = customtkinter.CTkButton(self.app, text='', image=PhotoImage(
            file='/home/pishexod/PycharmProjects/CassandraApp/add.png'), fg_color='#ffffff', hover_color='#ffffff',
                                                  height=15, width=15)
        self.keyspace = ''
        self.table = ''

    def center_window(self, width=500, height=500):
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (width / 2))
        y_cordinate = int((screen_height / 2) - (height / 2))
        self.app.geometry("{}x{}+{}+{}".format(width, height, x_cordinate, y_cordinate))

    def enter_keyspace(self, cassandra_cluster):
        self.cassandra_cluster = cassandra_cluster
        self.lable.configure(text='Введіть назву keyspace')
        self.entry.configure(placeholder_text='Keyspace')
        self.button.configure(text='Додати', command=self.add_keyspace)
        self.lable.pack()
        self.entry.pack()
        self.button.pack()

    def add_keyspace(self):
        self.cassandra_cluster.add_keyspace(self.entry.get())
        self.app.destroy()

    def cb_delete_keyspace(self, keyspaces, cassandra_cluster):
        self.cassandra_cluster = cassandra_cluster
        self.lable.configure(text='Виберіть який keyspace ви хочете видалити')
        self.cb.configure(values=keyspaces)
        self.cb.set('Виберіть keyspace')
        self.button.configure(text='Видалити', command=self.drop_keyspace)
        self.lable.pack()
        self.cb.pack()
        self.button.pack()

    def drop_keyspace(self):
        try:
            self.cassandra_cluster.drop_keyspace(self.cb.get())
            self.app.destroy()
        except:
            self.lable.configure(text='Ви не можете це видалити')
            self.lable.update()

    def window_add_table(self, keyspace, cassandra_cluster):
        self.cassandra_cluster = cassandra_cluster
        self.keyspace = keyspace
        widget = WidgetForTable(self.app)
        self.widgets_to_add_table.append(widget)
        self.lable.configure(text=f'Додати таблицю в {keyspace}')
        self.button.configure(text='Додати', command=self.add_table)
        self.button_add.configure(command=self.add_widget_table)
        self.cb.configure(values=['1'])
        self.cb.set('PRIMARY KEY')
        lable = customtkinter.CTkLabel(self.app, text='Введіть назву таблиці:')
        self.entry.configure(placeholder_text='Table')
        self.lable.pack(side=TOP)
        lable.place(relx=0.1, rely=0.1)
        self.entry.place(relx=0.5, rely=0.1)
        widget.draw_widget()
        self.button.pack(side=BOTTOM)
        self.button_add.pack(side=BOTTOM)
        self.cb.pack(side=BOTTOM)

    def add_widget_table(self):
        widget = WidgetForTable(self.app)
        self.widgets_to_add_table.append(widget)
        widget.draw_widget(self.y_widget)
        self.y_widget += 0.1
        count_entry = [str(i + 1) for i in range(len(self.widgets_to_add_table))]
        self.cb.configure(values=count_entry)
        self.cb.update()

    def add_table(self):
        key_values = ''
        for i in range(len(self.widgets_to_add_table)):
            key_values += f'{self.widgets_to_add_table[i].entry_name_row.get()} {self.widgets_to_add_table[i].cb_types.get()}, '
        pk = self.widgets_to_add_table[int(self.cb.get()) - 1].entry_name_row.get()
        self.cassandra_cluster.add_table_in_keyspace(self.keyspace, self.entry.get(), key_values, pk)
        self.app.destroy()

    def cb_delete_table(self, keyspace, tables, cassandra_cluster):
        self.keyspace = keyspace
        self.cassandra_cluster = cassandra_cluster
        self.lable.configure(text='Виберіть яку таблицю ви хочете видалити')
        self.cb.configure(values=tables)
        self.cb.set('Виберіть table')
        self.button.configure(text='Видалити', command=self.drop_table)
        self.lable.pack()
        self.cb.pack()
        self.button.pack()

    def drop_table(self):
        try:
            self.cassandra_cluster.drop_table_in_keyspace(self.keyspace, self.cb.get())
            self.app.destroy()
        except:
            self.lable.configure(text='Ви не можете це видалити')
            self.lable.update()

class WidgetForTable:
    def __init__(self, app):
        self.list_types = ['blob', 'ascii', 'text', 'variant', 'int', 'uuid', 'timestamp', 'boolean', 'float', 'double',
                           'decimal', 'counter']
        self.entry_name_row = customtkinter.CTkEntry(app, placeholder_text='name')
        self.cb_types = customtkinter.CTkComboBox(app, values=self.list_types)
        self.cb_types.set('Виберіть type')

    def draw_widget(self, y=0.2):
        self.entry_name_row.place(relx=0.1, rely=y)
        self.cb_types.place(relx=0.5, rely=y)
