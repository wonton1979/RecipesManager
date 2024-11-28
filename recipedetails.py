import tkinter.ttk
from email.policy import default
from tkinter import *
from tkinter import ttk
import ttkbootstrap as ttkb
from centerscreen import CenterScreen
from PIL import ImageTk, Image
from ttkbootstrap.constants import *
from databaseconnection import ConnectDatabase


class RecipeDetails(ttkb.Toplevel):
    COLUMNS = ("Ingredient Name", "Amount")
    def __init__(self, parent, recipe_id:str):
        super().__init__(parent)
        self.recipe_id: str = recipe_id
        self.ingredient_list: dict  = {}
        self.window_width = 910
        self.window_height = 920
        self.start_point = CenterScreen(screen=self, win_width=self.window_width, win_height=self.window_height)
        self.start_x = self.start_point.start_x
        self.start_y = self.start_point.start_y
        self.geometry(
            f"{self.window_width}x{self.window_height}+{int(self.start_point.start_x)}+"
            f"{int(self.start_point.start_y) - 30}")
        self.title("Recipe Details")
        self.resizable(False, False)
        self.__get_recipe_data()


    def __load_frame(self):
        self.main_frame = ttkb.Frame(self, padding=15)
        self.main_frame.pack(fill=BOTH, expand=YES)
        self.features_notebook = ttkb.Notebook(self)
        self._load_widgets(self.main_frame)


    def _load_widgets(self, main_frame):
        style = ttk.Style()
        self.recipe_title = ttkb.Label(main_frame, text="",font=(default, 20, 'bold'), foreground='orange')
        self.picture_frame = ttkb.LabelFrame(main_frame, labelwidget=self.recipe_title, style="warning", height=100,
                                             borderwidth=20, labelanchor="n", )
        self.picture_frame.grid(row=0, column=0, columnspan=3, pady=10, sticky=W)
        self.picture_label_one = ttkb.Label(self.picture_frame, image=self.img_recipe_one, borderwidth=5,
                                            relief="groove")
        self.picture_label_one.grid(row=0, column=0, padx=(10, 10), pady=10, sticky=W)
        self.picture_label_two = ttkb.Label(self.picture_frame, image=self.img_recipe_two, borderwidth=5,
                                            relief="groove")
        self.picture_label_two.grid(row=0, column=1, padx=(10, 10), pady=10, sticky=W)
        self.picture_label_three = ttkb.Label(self.picture_frame, image=self.img_recipe_three, borderwidth=5,
                                              relief="groove")
        self.picture_label_three.grid(row=0, column=2, padx=(10, 10), pady=10, sticky=W)

        self.ingredient_frame = ttkb.LabelFrame(main_frame, text="Ingredient List", style="primary", height=100,
                                                borderwidth=20, labelanchor="n", )
        self.ingredient_frame.grid(row=1, column=0, pady=10, sticky=W)
        style.configure("Custom.Treeview", rowheight=22)
        style.configure("Custom.Treeview.Heading", foreground='orange', font=(default, 10))
        self.ingredient_list_table = ttk.Treeview(self.ingredient_frame, columns=RecipeDetails.COLUMNS,
                                                   show='headings', height=18, )
        self.ingredient_list_table.heading("Ingredient Name", text="Ingredient Name")
        self.ingredient_list_table.column("Ingredient Name", width=180, anchor=CENTER)
        self.ingredient_list_table.heading("Amount", text="Amount")
        self.ingredient_list_table.column("Amount", width=150, anchor=CENTER)
        self.ingredient_list_table.config(style='Custom.Treeview')
        self.update()
        self.ingredient_list_table.pack()
        self.insert_item()

        self.instructions_frame = ttkb.LabelFrame(main_frame, text="Cooking Instructions", style="success", height=111,
                                                  borderwidth=20, labelanchor="n", )
        self.instructions_frame.grid(row=1, column=1, columnspan=2, pady=10, sticky=W)
        self.instructions_text = Text(self.instructions_frame, height=28, width=60, wrap=WORD)
        self.instructions_text.pack()



    def __get_recipe_data(self):
        search_recipe_sql: str = "SELECT ingredient_id,amount,unit FROM recipe_ingredient where recipe_id = ?"
        search_ingredient: list  = ConnectDatabase(search_recipe_sql).execute_sql_with_values((self.recipe_id,))
        for ingredient in search_ingredient:
            ingredient_name_sql: str = "SELECT ingredient_name from ingredient where ingredient_id = ?"
            ingredient_name_search_result = ConnectDatabase(ingredient_name_sql).execute_sql_with_values((ingredient[0],))
            ingredient_unit_name_sql: str = "SELECT unit_name from unit where unit_id = ?"
            ingredient_unit_name_search_result = ConnectDatabase(ingredient_unit_name_sql).execute_sql_with_values((ingredient[2],))
            self.ingredient_list[ingredient_name_search_result[0][0].title()] = str(ingredient[1]) + " " + ingredient_unit_name_search_result[0][0]
        recipe_images_instructions_sql: str = "SELECT image_one,image_two,image_three,instructions,recipe_name FROM recipes where recipe_id = ?"
        images_instructions_result: list = ConnectDatabase(recipe_images_instructions_sql).execute_sql_with_values((self.recipe_id,))
        try:
            image_one = Image.open(images_instructions_result[0][0]).resize((250, 250))
            self.img_recipe_one = ImageTk.PhotoImage(image_one)
            image_two = Image.open(images_instructions_result[0][1]).resize((250, 250))
            self.img_recipe_two = ImageTk.PhotoImage(image_two)
            image_three = Image.open(images_instructions_result[0][2]).resize((250, 250))
            self.img_recipe_three = ImageTk.PhotoImage(image_three)
        except FileNotFoundError as e:
            print(e)
        self.__load_frame()  # Call Main frame class,set self as the parent container of main frame
        self.recipe_title.config(text=images_instructions_result[0][4].title())
        self.instructions_text.insert(END,images_instructions_result[0][3].capitalize())
        self.instructions_text.configure(state=DISABLED)


    def insert_item(self):
        for key, value in self.ingredient_list.items():
            self.ingredient_list_table.insert('', 'end', values=[key, value])
