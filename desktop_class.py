import customtkinter
import os
from threading import Thread
from cassandra_class import Cassandra

class CTkApp:
    def __init__(self, title):
        self.app = customtkinter.CTk()
        self.app.title(title)
        self.center_window()
        self.verify_button = customtkinter.CTkButton(self.app)
        self.verify_label = customtkinter.CTkLabel(self.app)
        self.entry_password = customtkinter.CTkEntry(self.app)
        self.entry_host = customtkinter.CTkEntry(self.app)
        self.progress_bar = customtkinter.CTkProgressBar(self.app)
        self.lable_cassandra_info = customtkinter.CTkLabel(self.app)
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
        except():
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
            self.lable_cassandra_info.place(relx=0.5, rely=0.03, anchor=customtkinter.CENTER)
        except():
            self.lable_cassandra_info.configure(text='Такого хоста не існує')
            self.lable_cassandra_info.place(relx=0.5, rely=0.01, anchor=customtkinter.CENTER)
