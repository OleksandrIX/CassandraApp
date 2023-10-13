import tkinter
from tkinter.ttk import *
import customtkinter
import os
from threading import Thread
from cassandra_class import Cassandra
from tkinter import *
from window import Window


class CTkApp:
    def __init__(self, title):
        self.app = customtkinter.CTk(fg_color='#ffffff')
        self.app.title(title)
        self.center_window()
        self.verify_button = customtkinter.CTkButton(self.app)
        self.verify_label = customtkinter.CTkLabel(self.app)
        self.entry_password = customtkinter.CTkEntry(self.app)
        self.entry_host = customtkinter.CTkEntry(self.app)
        self.progress_bar = customtkinter.CTkProgressBar(self.app)
        self.lable_cassandra_info = customtkinter.CTkLabel(self.app)
        self.list_box = Listbox(self.app)
        self.table_cassandra = Treeview(self.app)
        self.button_back = customtkinter.CTkButton(self.app, text='', image=PhotoImage(
            file=os.path.join(os.getcwd(), "img", "back.png")), fg_color='#ffffff', hover_color='#ffffff',
                                                   height=15, width=15)
        self.button_add = customtkinter.CTkButton(self.app, text='', image=PhotoImage(
            file=os.path.join(os.getcwd(), "img", "add.png")), fg_color='#ffffff', hover_color='#ffffff',
                                                  height=15, width=15)
        self.button_delete = customtkinter.CTkButton(self.app, text='Drop', fg_color='#ffffff', hover_color='#ffffff',
                                                     height=15, width=15)

        self.command_install_jdk = 'sh script_install_jdk.sh'
        self.command_install_cassandra = 'sh script_install_cassandra.sh'
        self.keyspace = ''
        self.table = ''

        self.cassandra_cluster = Cassandra()
        self.th = Thread(target=self.verify_installed_apps)

    def center_window(self, width=500, height=500):
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (width / 2))
        y_cordinate = int((screen_height / 2) - (height / 2))
        self.app.geometry("{}x{}+{}+{}".format(width, height, x_cordinate, y_cordinate))

    def start(self):
        self.app.mainloop()

    def verify_cassandra(self):
        self.verify_label.configure(text='Перевірити чи встановленна cassandra')

        self.verify_label.place(relx=0.5, rely=0.4, anchor=customtkinter.CENTER)
        self.verify_button.configure(text='Перевірити', command=self.enter_password, width=155)
        self.verify_button.place(relx=0.5, rely=0.51, anchor=customtkinter.CENTER)

    def enter_password(self):
        self.verify_label.configure(text='Введіть пароль')
        self.entry_password.configure(placeholder_text='Введіть пароль від root', width=155)
        self.entry_password.place(relx=0.5, rely=0.45, anchor=customtkinter.CENTER)
        self.verify_button.configure(command=self.verify_password)

    def verify_password(self):
        if self.entry_password.get() == '':
            self.verify_label.configure(text='Ви не ввели пароль')
            self.entry_password.configure(border_color='red', placeholder_text_color='red')
        else:
            self.verify_button.configure(command=self.th.start())
            self.verify_button.place_forget()
            self.entry_password.place_forget()
            self.progress_bar.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
            self.progress_bar.start()

    def verify_installed_apps(self):
        try:
            self.verify_label.configure(text='Йде завантаження...')
            if os.system('which java') != 0:
                os.system('echo %s|sudo -S %s' % (self.entry_password.get(), self.command_install_jdk))
                if os.system('which cassandra') != 0:
                    os.system('echo %s|sudo -S %s' % (self.entry_password.get(), self.command_install_cassandra))
                    print('CASSANDRA INSTALLED!!!')
                else:
                    print('CASSANDRA ALREADY INSTALLED!!!')
            elif os.system('which cassandra') != 0:
                print('JAVA ALREADY INSTALLED!!!')
                os.system('echo %s|sudo -S %s' % (self.entry_password.get(), self.command_install_cassandra))
                print('CASSANDRA INSTALLED!!!')
            else:
                print('JAVA AND CASSANDRA ALREADY INSTALLED!!!')

            self.progress_bar.stop()
            self.progress_bar.place_forget()
            self.verify_label.configure(text='Cassandra встановлена')
            self.verify_button.configure(text='Запустити', command=self.enter_host_cluster)
            self.verify_button.place(relx=0.5, rely=0.51, anchor=customtkinter.CENTER)
        except:
            self.progress_bar.stop()
            self.progress_bar.place_forget()
            self.verify_label.configure(text='Cassandra не встановлена')

    def enter_host_cluster(self):
        self.verify_label.configure(text='Введіть IP хоста')
        self.entry_host.configure(placeholder_text='IP host')
        self.entry_host.place(relx=0.5, rely=0.45, anchor=customtkinter.CENTER)
        self.verify_button.configure(text='Підключитися', command=self.connect_to_db)

    def connect_to_db(self):
        self.entry_host.place_forget()
        self.verify_label.place_forget()
        self.verify_button.place_forget()
        try:
            self.cassandra_cluster.connect_cassandra(self.entry_host.get())
            self.lable_cassandra_info.configure(text=f'Host: {self.entry_host.get()}')
            self.lable_cassandra_info.pack()
            keyspaces = self.cassandra_cluster.get_all_keyspace()
            self.list_box.configure(listvariable=Variable(value=keyspaces), borderwidth=0, border=0, height=500)
            self.list_box.pack(fill=BOTH)
            self.list_box.bind('<Double-1>', self.select_keyspace)
            self.button_add.configure(command=self.add_keyspace_window)
            self.button_add.place(relx=0.9, rely=0)
            self.button_delete.configure(command=self.delete_keyspace)
            self.button_delete.place(relx=0.8, rely=0)
        except:
            self.lable_cassandra_info.configure(text='Такого хоста не існує')
            self.lable_cassandra_info.pack()

    def select_keyspace(self, event):
        self.button_back.configure(command=self.back_to_list_keyspace)
        self.button_add.configure(command=self.add_table_of_keyspace)
        self.button_delete.configure(command=self.delete_table_of_keyspace)
        self.button_delete.update()
        self.button_add.update()
        self.button_back.place(relx=0.01, rely=0)
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.keyspace = event.widget.get(index)
            tables = self.cassandra_cluster.get_all_tables_of_keyspace(self.keyspace)
            self.list_box.configure(listvariable=Variable(value=tables))
            self.list_box.bind('<Double-1>', self.select_table_of_keyspace)
            self.list_box.update()
            self.lable_cassandra_info.configure(text=f'{self.lable_cassandra_info.text} \n Keyspace: {self.keyspace}')
            self.lable_cassandra_info.update()

    def select_table_of_keyspace(self, event):
        self.button_back.configure(command=self.back_to_list_table)
        self.button_add.configure(command=self.add_row_to_table)
        self.button_delete.configure(command=self.delete_row_to_table)
        self.button_delete.update()
        self.button_add.update()
        self.button_back.update()
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.table = event.widget.get(index)
            self.lable_cassandra_info.configure(text=f'{self.lable_cassandra_info.text} \n Table: {self.table}')
            self.lable_cassandra_info.update()
            self.list_box.pack_forget()
            self.draw_table()

    def draw_table(self):
        self.table_cassandra.delete(*self.table_cassandra.get_children())
        columns = list(self.cassandra_cluster.get_all_column_of_table(self.keyspace, self.table))
        pk_name = self.cassandra_cluster.get_pk_of_table(self.keyspace, self.table)
        self.table_cassandra.configure(columns=columns, show='headings', height=500)
        for i in range(len(columns)):
            if pk_name == columns[i]:
                self.table_cassandra.heading(columns[i], text=f'{columns[i]} (pk)')
            else:
                self.table_cassandra.heading(columns[i], text=columns[i])
        info_of_columns = self.cassandra_cluster.get_info_of_column(self.keyspace, self.table)
        print(info_of_columns)
        for i in range(len(info_of_columns)):
            self.table_cassandra.insert('', tkinter.END, values=info_of_columns[i])
        self.table_cassandra.pack(fill=BOTH)

    def back_to_list_keyspace(self):
        self.button_back.place_forget()
        self.lable_cassandra_info.configure(text=f'Host: {self.entry_host.get()}')
        self.lable_cassandra_info.pack()
        keyspaces = self.cassandra_cluster.get_all_keyspace()
        self.list_box.configure(listvariable=Variable(value=keyspaces), borderwidth=0, border=0)
        self.list_box.bind('<Double-1>', self.select_keyspace)
        self.list_box.pack(fill=BOTH)
        self.button_add.configure(command=self.add_keyspace_window)
        self.button_add.place(relx=0.9, rely=0)

    def back_to_list_table(self):
        self.button_back.configure(command=self.back_to_list_keyspace)
        self.button_back.update()
        self.lable_cassandra_info.configure(text='')
        self.lable_cassandra_info.configure(text=f'Host: {self.entry_host.get()} \n Keyspace: {self.keyspace}')
        self.lable_cassandra_info.update()
        self.table_cassandra.pack_forget()
        tables = self.cassandra_cluster.get_all_tables_of_keyspace(self.keyspace)
        self.list_box.configure(listvariable=Variable(value=tables))
        self.list_box.bind('<Double-1>', self.select_table_of_keyspace)
        self.list_box.pack(fill=BOTH)

    def add_keyspace_window(self):
        window = Window(self.app, 200, 90, 'Add Keyspace')
        window.enter_keyspace(self.cassandra_cluster)
        window.app.wait_window()
        self.update_list_keyspace()

    def delete_keyspace(self):
        window = Window(self.app, 300, 130, 'Delete Keyspace')
        keyspaces = self.cassandra_cluster.get_all_keyspace()
        window.cb_delete_keyspace(keyspaces, self.cassandra_cluster)
        window.app.wait_window()
        self.update_list_keyspace()

    def update_list_keyspace(self):
        keyspaces = self.cassandra_cluster.get_all_keyspace()
        self.list_box.configure(listvariable=Variable(value=keyspaces), borderwidth=0, border=0, height=500)
        self.list_box.pack(fill=BOTH)
        self.list_box.bind('<Double-1>', self.select_keyspace)

    def add_table_of_keyspace(self):
        window = Window(self.app, 400, 300, 'Add Table')
        window.window_add_table(self.keyspace, self.cassandra_cluster)
        window.app.wait_window()
        self.update_list_table()

    def delete_table_of_keyspace(self):
        window = Window(self.app, 300, 130, 'Delete Table')
        tables = self.cassandra_cluster.get_all_tables_of_keyspace(self.keyspace)
        window.cb_delete_table(self.keyspace, tables, self.cassandra_cluster)
        window.app.wait_window()
        self.update_list_table()

    def update_list_table(self):
        tables = self.cassandra_cluster.get_all_tables_of_keyspace(self.keyspace)
        self.list_box.configure(listvariable=Variable(value=tables))
        self.list_box.bind('<Double-1>', self.select_table_of_keyspace)
        self.list_box.pack(fill=BOTH)

    def add_row_to_table(self):
        window = Window(self.app, 400, 300, 'Add Row')
        window.window_add_row(self.keyspace, self.table, self.cassandra_cluster)
        window.app.wait_window()
        self.table_cassandra.delete()
        self.draw_table()

    def delete_row_to_table(self):
        window = Window(self.app, 300, 130, 'Delete Row')
        pk_key = self.cassandra_cluster.get_pk_of_table(self.keyspace, self.table)
        pk_values = self.cassandra_cluster.get_all_pk_value(self.keyspace, self.table, pk_key)
        window.cb_delete_row(self.keyspace, self.table, pk_key, pk_values, self.cassandra_cluster)
        window.app.wait_window()
        self.table_cassandra.delete()
        self.draw_table()
