import customtkinter
from tkinter import *
import os

class Window:
    def __init__(self, parent, width, height, name):
        self.app = customtkinter.CTkToplevel(parent)
        self.center_window(width, height)
        self.app.title(name)
        self.lable = customtkinter.CTkLabel(self.app)
        self.entry = customtkinter.CTkEntry(self.app)
        self.button = customtkinter.CTkButton(self.app)
        self.cb = customtkinter.CTkComboBox(self.app)
        self.cassandra_cluster = None
        self.y_widget = 0.3
        self.widgets_to_add_table = []
        self.widgets_to_add_row = []
        self.button_add = customtkinter.CTkButton(self.app, text='', image=PhotoImage(
            file=os.path.join(os.getcwd(), "img", "add.png")), fg_color='#ffffff', hover_color='#ffffff',
                                                  height=15, width=15)
        self.keyspace = ''
        self.table = ''
        self.pk_key = ''

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

    def window_add_row(self, keyspace, table, cassandra_cluster):
        self.cassandra_cluster = cassandra_cluster
        self.keyspace = keyspace
        self.table = table
        self.lable.configure(text=f'Додати рядок в {table}')
        self.button.configure(text='Додати', command=self.add_row)
        columns_name = list(self.cassandra_cluster.get_all_column_of_table(self.keyspace, self.table))
        self.y_widget = 0.2
        for i in range(len(columns_name)):
            widget = WidgetForAddRow(self.app, columns_name[i])
            widget.draw_widget(self.y_widget)
            self.widgets_to_add_row.append(widget)
            self.y_widget += 0.1
        self.lable.pack(side=TOP)
        self.button.pack(side=BOTTOM)

    def add_row(self):
        columns_name = ''
        columns_value = ''
        result = list(self.cassandra_cluster.get_all_column_of_table(self.keyspace, self.table))
        columns_text = self.cassandra_cluster.get_name_column_of_text(self.keyspace, self.table)
        for i in range(len(result)):
            if i == len(result) - 1:
                columns_name += result[i]
            else:
                columns_name += f'{result[i]}, '

        for i in range(len(result)):
            for j in range(len(columns_text)):
                if i == len(result) - 1:
                    if result[i] == columns_text[j]:
                        columns_value += f"'{self.widgets_to_add_row[i].entry.get()}'"
                        columns_text.__delitem__(0)
                        break
                    else:
                        columns_value += f"{self.widgets_to_add_row[i].entry.get()}"
                else:
                    if result[i] == columns_text[j]:
                        columns_value += f"'{self.widgets_to_add_row[i].entry.get()}', "
                        columns_text.__delitem__(0)
                        break
                    else:
                        columns_value += f"{self.widgets_to_add_row[i].entry.get()}, "
        if len(columns_text) == 0:
            if i == len(result) - 1:
                columns_value += f"{self.widgets_to_add_row[i].entry.get()}"
            else:
                columns_value += f"{self.widgets_to_add_row[i].entry.get()}, "

        self.cassandra_cluster.add_row_in_table(self.keyspace, self.table, columns_name, columns_value)
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

    def cb_delete_row(self, keyspace, table, pk_key, pk_values, cassandra_cluster):
        self.keyspace = keyspace
        self.table = table
        self.pk_key = pk_key
        self.cassandra_cluster = cassandra_cluster
        self.lable.configure(text='Виберіть який рядок ви хочете видалити')
        self.cb.configure(values=pk_values)
        self.cb.set('Виберіть рядок')
        self.button.configure(text='Видалити', command=self.delete_row)
        self.lable.pack()
        self.cb.pack()
        self.button.pack()

    def delete_row(self):
        try:
            self.cassandra_cluster.drop_row_in_table(self.keyspace, self.table, self.pk_key, self.cb.get())
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


class WidgetForAddRow:
    def __init__(self, app, name):
        self.lable = customtkinter.CTkLabel(app, text=name)
        self.entry = customtkinter.CTkEntry(app, placeholder_text=name)

    def draw_widget(self, y=0.2):
        self.lable.place(relx=0.1, rely=y)
        self.entry.place(relx=0.5, rely=y)
