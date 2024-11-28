import tkinter
from tkinter import *
import ttkbootstrap as ttkb
from ttkbootstrap import Style
from centerscreen import CenterScreen
from mainwindow import MainWindow
from ttkbootstrap.dialogs import Messagebox
from databaseconnection import ConnectDatabase
from inputvalidate import InputValidate


class UserRegister(ttkb.Toplevel):
    DIET_CATEGORY: tuple = ('Flexitarian (Normal Diet)',
                            'Pescatarian',
                            'Lacto-ovo-vegetarian',
                            'Lacto-vegetarian',
                            'Ovo-vegetarian',
                            'Vegan',)
    COMMON_FOOD_ALLERGY: tuple = ('Tree Nuts', 'Seafood And Shellfish', 'Peanuts', 'Milk', 'Eggs', 'Soy',
                                  'Fish', 'Grain Product', 'Sesame')

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title('New User Register')
        self.window_width: int = 355
        self.window_height: int = 500
        self.start_point: CenterScreen = CenterScreen(screen=self, win_width=self.window_width,
                                                      win_height=self.window_height)
        self.start_x: int = self.start_point.start_x
        self.start_y: int = self.start_point.start_y
        self.geometry(
            f"{self.window_width}x{self.window_height}+{int(self.start_point.start_x)}+"
            f"{int(self.start_point.start_y) - 30}")
        self.list_index: int = 0
        self.allergy_list: list = []
        self.__user_register_widgets()
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.mainloop()

    def __user_register_widgets(self):
        self.main_frame = ttkb.Frame(self, )
        self.main_frame.pack(fill=BOTH, expand=True, padx=(15, 0))
        Style(theme='superhero')
        self.user_name_label = ttkb.Label(self.main_frame, text="Username :")
        self.user_name_label.grid(column=0, row=0, padx=10, pady=(30, 10), sticky='w')
        self.user_name_entry = ttkb.Entry(self.main_frame, width=25, style='primary')
        self.user_name_entry.grid(column=1, row=0, padx=10, pady=(30, 10), columnspan=2, sticky='w')
        self.user_name_entry.focus()
        self.user_password_label = ttkb.Label(self.main_frame, text="Password :")
        self.user_password_label.grid(column=0, row=1, padx=10, pady=10, sticky='w')
        self.user_password_entry = ttkb.Entry(self.main_frame, show="*", width=25, style='primary')
        self.user_password_entry.grid(column=1, row=1, padx=10, pady=10, columnspan=2, sticky='w')
        self.user_email_label = ttkb.Label(self.main_frame, text="Email :")
        self.user_email_label.grid(column=0, row=2, padx=10, pady=10, sticky='w')
        self.user_email_entry = ttkb.Entry(self.main_frame, width=25, style='primary')
        self.user_email_entry.grid(column=1, row=2, padx=10, pady=10, columnspan=2, sticky='w')
        self.user_diet_preference_label = ttkb.Label(self.main_frame, text="Diet Preference :")
        self.user_diet_preference_label.grid(column=0, row=3, padx=10, pady=10, sticky='w')
        self.user_diet_preference_combo = ttkb.Combobox(self.main_frame, values=UserRegister.DIET_CATEGORY,
                                                        state='readonly', width=23, style='primary')
        self.user_diet_preference_combo.grid(column=1, row=3, padx=10, pady=10, columnspan=2, sticky='w')
        self.user_diet_preference_combo.current(0)
        self.user_halal_food_label = ttkb.Label(self.main_frame, text="Halal Food :")
        self.user_halal_food_label.grid(column=0, row=4, padx=10, pady=10, sticky='w')
        self.user_halal_food_combo = ttkb.Combobox(self.main_frame, values=('No', 'Yes'),
                                                   state='readonly', width=23, style='primary')
        self.user_halal_food_combo.grid(column=1, row=4, padx=10, pady=10, columnspan=2, sticky='w')
        self.user_halal_food_combo.current(0)
        self.user_food_allergy_label = ttkb.Label(self.main_frame, text="Any Food Allergy ?")
        self.user_food_allergy_label.grid(column=0, row=5, padx=10, pady=10, sticky='w')
        self.user_food_allergy_combo = ttkb.Combobox(self.main_frame, values=self.COMMON_FOOD_ALLERGY, state='readonly',
                                                     width=16,
                                                     justify='center', style='primary')
        self.user_food_allergy_combo.grid(column=1, row=5, padx=10, pady=10, columnspan=2, sticky='w')
        self.user_food_allergy_combo.current(2)
        self.add_food_allergy = ttkb.Button(self.main_frame, text="+", command=self.add_to_allergy_list)
        self.add_food_allergy.grid(column=2, row=5, padx=(30, 10), pady=10, sticky='e')
        self.food_allergy_list_table = ttkb.Treeview(self.main_frame, columns=('Index', 'Food Allergy List',),
                                                     show='headings',
                                                     height=5)
        self.food_allergy_list_table.heading("Index", text="Index")
        self.food_allergy_list_table.column("Index", width=100, anchor=CENTER)
        self.food_allergy_list_table.heading("Food Allergy List", text="Your Food Allergy List")
        self.food_allergy_list_table.column("Food Allergy List", width=200, anchor=CENTER)
        self.food_allergy_list_table.grid(column=0, row=6, padx=10, pady=10, columnspan=3, sticky='w')
        self.register_new_user = ttkb.Button(self.main_frame, text="Create Account", style='success',
                                             command=self.input_data_validation)
        self.register_new_user.grid(column=0, row=7, padx=10, pady=10, sticky='w', ipadx=20, columnspan=2)
        self.reset_form_button = ttkb.Button(self.main_frame, text="Reset The From", style='success',
                                             command=self.reset_form)
        self.reset_form_button.grid(column=2, row=7, padx=10, pady=10, sticky='w', ipadx=17)

    def register_user_success(self):
        self.withdraw()
        self.parent.deiconify()

    def add_to_allergy_list(self):
        if self.user_food_allergy_combo.get() not in self.allergy_list:
            self.allergy_list.append(self.user_food_allergy_combo.get())
            self.food_allergy_list_table.insert('', index='end', values=[self.list_index + 1,
                                                                         self.allergy_list[self.list_index], ])
            self.list_index += 1
        else:
            Messagebox.show_error(parent=self, title="Error Message",
                                  message='This item has been added to your allergy already !')

    def reset_form(self):
        self.user_name_entry.delete('0', END)
        self.user_password_entry.delete('0', END)
        self.user_email_entry.delete('0', END)
        for row in self.food_allergy_list_table.get_children():
            self.food_allergy_list_table.delete(row)
        self.user_diet_preference_combo.current(0)
        self.user_food_allergy_combo.current(0)

    def input_data_validation(self):
        user_exist_check = ConnectDatabase(sql_query='select * from users where email=? or username=?', )
        user_exist_check_result = user_exist_check.execute_sql_with_values((self.user_email_entry.get().strip().lower(),
                                                                            self.user_name_entry.get().strip().lower()))
        if len(user_exist_check_result) == 0:
            total_field_check_passed: int = 0
            allergy_food_type_id_list: list = []
            password_check_result: dict = InputValidate(self.user_password_entry.get().strip()).check_password()
            if not password_check_result['password_ok'][0]:
                for value in password_check_result.values():
                    if value[0]:
                        password_error_message = value[1]
                        break
            user_details_check: dict = {
                'username': [InputValidate(self.user_name_entry.get().strip().lower(), ).check_text_number() and
                             3 < len(self.user_name_entry.get().strip().lower(), ) < 12,
                             'Your username should only use letter and number and between 3 to 12 long !'],
                'password': [password_check_result['password_ok'][0],
                             '1. Your Password should between 8 and 15 characters long ! \n '
                             '2. Your Password should include at least one Up case and one Lower case letter !\n'
                             '3. Your Password should include at least one Number ! \n '
                             '4. Your Password should include at least special symbol from this list ( !,#,$,%,&,*,@ ) !'],
                'email': [InputValidate(self.user_email_entry.get().strip().lower()).check_email(),
                          'Please input a valid email address !'],
            }
            for key, value in user_details_check.items():
                if not value[0]:
                    Messagebox.show_error(parent=self, title="Error Message",
                                          message=f'{key.title()} Error :\n {value[1]}')
                else:
                    total_field_check_passed += 1

            if total_field_check_passed == 3:
                if len(self.food_allergy_list_table.get_children()) == 0:
                    user_selection: Messagebox = Messagebox.yesno(parent=self, title="Confirmation Needed",
                                                                  message="Can you confirm that your don't have any "
                                                                          "food allergy ?")
                    if user_selection == 'no':
                        Messagebox.show_info(parent=self, title="Information",
                                             message="Please add the food allergy item(s) to the "
                                                     "table !")
                    else:
                        total_field_check_passed += 1
                else:
                    total_field_check_passed += 1

            if total_field_check_passed == 4:
                sql_register_user: str = ('insert into users (username, password, email,diet_preference, halal_food) '
                                          'values(?,?,?,?,?)')
                register_user = ConnectDatabase(sql_register_user)
                if len(self.allergy_list) == 0:
                    register_user.execute_insert_query(
                        (self.user_name_entry.get().lower(), self.user_password_entry.get(),
                         self.user_email_entry.get().strip().lower(),
                         self.user_diet_preference_combo.get(), self.user_halal_food_combo.get(),))
                    Messagebox.show_info(parent=self, title='Information',
                                         message='Your details has registered successfully, '
                                                 'You can now login to application !')
                    self.reset_form()
                    self.close_window()
                else:
                    register_user.execute_insert_query(
                        (self.user_name_entry.get().lower(), self.user_password_entry.get(),
                         self.user_email_entry.get().strip().lower(),
                         self.user_diet_preference_combo.get(), self.user_halal_food_combo.get(),))
                    user_id_check = ConnectDatabase(sql_query='select user_id from users where email=? and username=?')
                    user_id_check_result = user_id_check.execute_sql_with_values((self.user_email_entry.get().strip().lower(),
                                                                                  self.user_name_entry.get().strip().lower()))
                    print(self.allergy_list)
                    for each_allergy_type in self.allergy_list:
                        type_id_check_sql: str = 'select type_id from food_type_list where type_name=?'
                        type_id_check_result = ConnectDatabase(type_id_check_sql).execute_sql_with_values((each_allergy_type,))
                        sql_add_user_allergy: str = 'insert into user_allergy_list (user_id, allergy_type) values(?,?)'
                        print(user_id_check_result[0][0],type_id_check_result[0][0])
                        ConnectDatabase(sql_add_user_allergy).execute_insert_query((user_id_check_result[0][0], type_id_check_result[0][0],))
                    Messagebox.show_info(parent=self, title='Information',
                                         message='Your details has registered successfully, '
                                                 'You can now login to application !')
                    self.reset_form()
                    self.close_window()


        else:
            Messagebox.show_error(parent=self, title="Error Message",
                                  message='Username or Email exist already,Please change your details !')

    def close_window(self):
        self.withdraw()
        self.parent.deiconify()
        self.parent.username_entry.focus()


if __name__ == '__main__':
    UserRegister('')
