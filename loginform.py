from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from databaseconnection import ConnectDatabase
from centerscreen import CenterScreen
from mainwindow import MainWindow
import ttkbootstrap as ttkb
from ttkbootstrap import Style
from userregister import UserRegister
from recipemanagement import RecipeManagement


class LoginForm(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.window_width: int = 440
        self.window_height: int = 350
        self.start_point: CenterScreen = CenterScreen(screen=self, win_width=self.window_width,
                                                      win_height=self.window_height)
        self.start_x: int = self.start_point.start_x
        self.start_y: int = self.start_point.start_y
        self.geometry(
            f"{self.window_width}x{self.window_height}+{int(self.start_point.start_x)}+{int(self.start_point.start_y)}")
        self.title("Recipe Manager")
        self.configure(bg="#83d2c5")
        self.resizable(False, False)
        image = Image.open("Images/recipe_manager.png").resize((261, 176))
        img_lego = ImageTk.PhotoImage(image)
        self.admin_login_check : bool = False
        self.__load_widgets(img_lego)
        self.mainloop()

    def __load_widgets(self, img_lego):
        self.main_frame = ttkb.Frame(self, )
        self.main_frame.pack(fill=BOTH, expand=True)
        Style('superhero')
        pic_label = Label(self.main_frame, image=img_lego, borderwidth=0)
        pic_label.grid(row=0, column=0, columnspan=3, padx=97, pady=15, sticky='nsew')
        username_label = Label(self.main_frame, text="Username :", bg="#83d2c5", fg="Black", font=('KaiTi', 12),
                               anchor="e")
        username_label.grid(row=1, column=0, padx=(10, 22), sticky='nsew', pady=(0, 15), )
        self.username_entry = Entry(self.main_frame, width=32, bd=3)
        self.username_entry.focus()
        self.username_entry.grid(row=1, column=1, sticky='W', pady=(0, 15), columnspan=2)
        password_label = Label(self.main_frame, text="Password :", bg="#83d2c5", fg="Black", font=('KaiTi', 12),
                               anchor="e")
        password_label.grid(row=2, column=0, padx=(10, 22), sticky='nsew')
        self.password_entry = Entry(self.main_frame, width=32, bd=3, show='*')
        self.password_entry.grid(row=2, column=1, sticky='w', columnspan=2)
        login_button = Button(self.main_frame, text="Login",
                              command=lambda: self._security_check(self.username_entry.get(),
                                                                   self.password_entry.get()))
        self.bind('<Return>', self._call_bridge)
        login_button.grid(row=3, column=0, pady=25, ipadx=15, ipady=5, sticky=E, padx=(0, 39))
        register_button = Button(self.main_frame, text="Register", command=self._register_new_user)
        register_button.grid(row=3, column=1, pady=25, ipadx=10, ipady=5, sticky=W, padx=(12, 0))
        exit_button = Button(self.main_frame, text="Exit", command=self.destroy, )
        exit_button.grid(row=3, column=2, padx=(0, 32), pady=25, ipadx=22, ipady=5, sticky=W)

    def _call_bridge(self, _event=None):
        self._security_check(self.username_entry.get(), self.password_entry.get())

    def _security_check(self, username, password):
        query = ConnectDatabase("select username,password,admin_account,user_id from users where username = ? and password = ?")
        query_result = query.execute_sql_with_values((username.lower(), password))
        if len(query_result) == 0:
            messagebox.showwarning(title="Login Failed", message="Incorrect Username or Password !")
            self.username_entry.delete(0,END)
            self.password_entry.delete(0,END)
            self.username_entry.focus()
        else:
            if query_result[0][2] != 1:
                query.close_connect()
                self.username_entry.delete('0', END)
                self.password_entry.delete('0', END)
                self.withdraw()
                MainWindow(self,query_result[0][3])
            else:
                query.close_connect()
                self.username_entry.delete('0', END)
                self.password_entry.delete('0', END)
                self.withdraw()
                RecipeManagement(self)

    def _register_new_user(self):
        self.withdraw()
        UserRegister(self)


if __name__ == '__main__':
    LoginForm()
