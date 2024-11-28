import tkinter
from tkinter import *
from email.policy import default
from tkinter import ttk
import tkinter as tk
import ttkbootstrap as ttkb
from fontTools.ttLib.tables.ttProgram import instructions

from centerscreen import CenterScreen
from ttkbootstrap.constants import *
from databaseconnection import ConnectDatabase
from inputvalidate import InputValidate
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog
from imagereview import ImageReview
from PIL import Image
import os
import shutil


class RecipeManagement(ttkb.Toplevel):
    SERVING_TYPE: tuple = ('Breakfast', 'Lunch', 'Dinner')
    DIET_CATEGORY: tuple = ('Flexitarian (Normal Diet)','Vegan')
    COOKING_TIME: tuple = (
        '10 - 30 Minutes', '31 - 45 Minutes', '46 - 60 Minutes', '60 - 90 Minutes', '91 - 120 Minutes')
    COLUMNS: tuple = ("Ingredient Name", "Amount","Food Type ID")
    UNIT: tuple = ('Gram', 'Ml', 'Tablespoon', 'Unit', 'Pinch')
    INGREDIENT_TYPE: tuple = (
        'Meat', 'Poultry', 'Fish', 'Seafood And Shellfish', 'Vegetables', 'Dairy Product', 'Cooking Oil', 'Nuts', 'Egg',
        'Fruit', 'Grain Product', 'Seasoning', 'Soy', 'Sesame', 'Yeast', 'Water', 'Cocoa Product', 'Dry Fruit','Tree Nuts')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.search_result = None
        self.parent = parent
        self.result_index = 0
        self.window_width: int = 1110
        self.window_height: int = 760
        self.start_point: CenterScreen = CenterScreen(screen=self, win_width=self.window_width,
                                                      win_height=self.window_height)
        self.start_x: int = self.start_point.start_x
        self.start_y: int = self.start_point.start_y
        self.ingredient_items_list: list = []
        self.amend_ingredient_items_list: list = []
        self.current_recipe_id: int = -1
        self.geometry(
            f"{self.window_width}x{self.window_height}+{int(self.start_point.start_x)}+"
            f"{int(self.start_point.start_y) - 30}")
        self.title("Recipe Resource Management")
        self.resizable(False, False)
        self.attributes('-topmost', 1)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.ingredient_table_iid_number: str = ''
        self.__load_frame()

    def __load_frame(self):
        ttk.Style()
        self.selected_value = tk.StringVar()
        self.selected_value.set('1')
        self.add_new_frame = ttkb.Frame(self, padding=25)
        self.add_new_frame.pack(fill=BOTH, expand=YES)

        self.amend_exist_frame = ttkb.Frame(self, padding=25)
        self.amend_exist_frame.pack(fill=BOTH, expand=YES)

        """
            Interface for General Frame's Widgets
        """
        self.general_frame = ttkb.LabelFrame(self.add_new_frame, text="General Information", style="warning",
                                             height=100,
                                             borderwidth=34, labelanchor="n", )
        self.general_frame.grid(row=0, column=0, padx=(5, 0), pady=(15, 0), sticky=W, columnspan=2)
        self.title_label = ttkb.Label(self.general_frame, text="Recipe Name :")
        self.title_label.grid(column=0, row=0, padx=(5, 0), pady=10)
        self.title_entry = ttkb.Entry(self.general_frame, width=30, style="success")
        self.title_entry.grid(column=1, row=0, padx=(5, 5), pady=10, )
        self.serving_type_label = ttkb.Label(self.general_frame, text="Serving Type :")
        self.serving_type_label.grid(column=0, row=1, padx=5, pady=10)
        self.serving_type_combo = ttkb.Combobox(self.general_frame, values=RecipeManagement.SERVING_TYPE, style="success",
                                                width=28, justify="center", state="readonly")
        self.serving_type_combo.current(2)
        self.serving_type_combo.grid(column=1, row=1, padx=5, pady=10)
        self.halal_food_label = ttkb.Label(self.general_frame, text="Is This Halal Food   :")
        self.halal_food_label.grid(column=2, row=0, padx=(7, 15), pady=10)
        self.halal_yes_radiobutton = ttkb.Radiobutton(self.general_frame, style="success", text="Yes", value=1,
                                                      variable=self.selected_value)
        self.halal_yes_radiobutton.grid(column=3, row=0, padx=10, pady=10)
        self.halal_no_radiobutton = ttkb.Radiobutton(self.general_frame, style="danger", text="No", value=0,
                                                     variable=self.selected_value)
        self.halal_no_radiobutton.grid(column=4, row=0, padx=10, pady=10)
        self.category_label = ttkb.Label(self.general_frame, text="Diet Category :")
        self.category_label.grid(column=0, row=2, padx=5, pady=10)
        self.diet_category_combo = ttkb.Combobox(self.general_frame, values=RecipeManagement.DIET_CATEGORY, style="success",
                                                 width=28, justify="center", state="readonly")
        self.diet_category_combo.current(0)
        self.diet_category_combo.grid(column=1, row=2, padx=5, pady=10)
        self.cooking_time_label = ttkb.Label(self.general_frame, text="Cooking Time         :")
        self.cooking_time_label.grid(column=2, row=1, padx=(7, 15), pady=10)
        self.cooking_time_entry = ttkb.Entry(self.general_frame,style="success",width=21, justify="center",)
        self.cooking_time_entry.grid(column=3, row=1, padx=(0, 5), pady=10, columnspan=2)

        self.calories_label = ttkb.Label(self.general_frame, text="Calories Per Serving :")
        self.calories_label.grid(column=2, row=2, padx=(7, 15), pady=10)
        self.calories_entry = ttkb.Entry(self.general_frame, width=24, style="success",justify='center')
        self.calories_entry.grid(column=3, row=2, padx=(0, 5), pady=10, columnspan=2)

        self.recipe_picture_one_label = ttkb.Label(self.general_frame, text="Image One  :")
        self.recipe_picture_one_label.grid(column=0, row=3, padx=(7, 15), pady=10)
        self.recipe_picture_one_entry = ttkb.Entry(self.general_frame, width=60, style="success")
        self.recipe_picture_one_entry.grid(column=1, row=3, pady=10, padx=(5, 0), columnspan=3, sticky='w')
        self.picture_one_directory_button = ttkb.Button(self.general_frame, text="Select File", style="success,outline",
                                                        width=15, command=lambda: self.get_file_directory('one','add'))
        self.picture_one_directory_button.grid(column=4, row=3, padx=(0, 26), pady=10)

        self.recipe_picture_two_label = ttkb.Label(self.general_frame, text="Image Two  :")
        self.recipe_picture_two_label.grid(column=0, row=4, padx=(7, 15), pady=10)
        self.recipe_picture_two_entry = ttkb.Entry(self.general_frame, width=60, style="success")
        self.recipe_picture_two_entry.grid(column=1, row=4, pady=10, padx=(5, 0), columnspan=3, sticky='w')
        self.picture_two_directory_button = ttkb.Button(self.general_frame, text="Select File", style="success,outline",
                                                        width=15, command=lambda: self.get_file_directory('two','add'))
        self.picture_two_directory_button.grid(column=4, row=4, pady=10, padx=(0, 26))

        self.recipe_picture_three_label = ttkb.Label(self.general_frame, text="Image Three :")
        self.recipe_picture_three_label.grid(column=0, row=5, padx=(7, 15), pady=10)
        self.recipe_picture_three_entry = ttkb.Entry(self.general_frame, width=60, style="success")
        self.recipe_picture_three_entry.grid(column=1, row=5, pady=10, padx=(5, 0), columnspan=3, sticky='w')
        self.picture_three_directory_button = ttkb.Button(self.general_frame, text="Select File",
                                                          style="success,outline",
                                                          width=15, command=lambda: self.get_file_directory('three','add'))
        self.picture_three_directory_button.grid(column=4, row=5, pady=10, padx=(0, 26))

        # Interface for Ingredient Frame's Widgets
        self.ingredient_frame = ttkb.LabelFrame(self.add_new_frame, text="Ingredient List", style="warning", height=100,
                                                borderwidth=20, labelanchor="n", )
        self.ingredient_frame.grid(row=1, column=0, padx=(5, 0), pady=(30, 0), sticky=W)

        self.ingredient_name_label = ttkb.Label(self.ingredient_frame, text="Name :")
        self.ingredient_name_label.grid(column=0, row=0, padx=7, pady=6, sticky='w', )
        self.ingredient_name_entry = ttkb.Entry(self.ingredient_frame, width=17, style='primary')
        self.ingredient_name_entry.grid(column=1, row=0, padx=7, pady=6, sticky='w', columnspan=3)
        self.ingredient_amount_label = ttkb.Label(self.ingredient_frame, text="Amount :")
        self.ingredient_amount_label.grid(column=2, row=0, padx=7, pady=6, sticky='w')
        self.ingredient_amount_entry = ttkb.Entry(self.ingredient_frame, width=17, style='primary')
        self.ingredient_amount_entry.grid(column=3, row=0, padx=7, pady=6, sticky='w')

        self.ingredient_unit_label = ttkb.Label(self.ingredient_frame, text="Unit :")
        self.ingredient_unit_label.grid(column=0, row=1, padx=7, pady=6, sticky='w')
        self.ingredient_unit_combo = ttkb.Combobox(self.ingredient_frame, values=RecipeManagement.UNIT, style="primary",
                                                   width=15, justify="center", state="readonly")
        self.ingredient_unit_combo.current(0)
        self.ingredient_unit_combo.grid(column=1, row=1, padx=7, pady=6, sticky='w')

        self.ingredient_type_label = ttkb.Label(self.ingredient_frame, text="Type :")
        self.ingredient_type_label.grid(column=2, row=1, padx=7, pady=6, sticky='w')
        self.ingredient_type_combo = ttkb.Combobox(self.ingredient_frame, values=RecipeManagement.INGREDIENT_TYPE,
                                                   style="primary",
                                                   width=15, justify="center", state="readonly")
        self.ingredient_type_combo.current(0)
        self.ingredient_type_combo.grid(column=3, row=1, padx=7, pady=6, sticky='w')

        self.add_new_ingredient_button = ttkb.Button(self.ingredient_frame, text="Add New Ingredient",
                                                     style="outline", width=25, command=self.ingredient_data_validate,
                                                     )
        self.add_new_ingredient_button.grid(row=2, column=0, columnspan=2, padx=(10, 0), pady=(9, 0), sticky='w', )
        self.delete_ingredient_button = ttkb.Button(self.ingredient_frame, text="Delete Ingredient",
                                                    style="outline", width=25, command=self.ingredient_table_row_delete,
                                                    state=tk.DISABLED)
        self.delete_ingredient_button.grid(row=2, column=2, columnspan=2, padx=(11, 0), pady=(9, 0), sticky='w')

        self.ingredient_list_table = ttkb.Treeview(self.ingredient_frame, columns=RecipeManagement.COLUMNS, show='headings',
                                                   height=5)
        self.ingredient_list_table.heading("Ingredient Name", text="Ingredient Name")
        self.ingredient_list_table.column("Ingredient Name", width=150, anchor=CENTER)
        self.ingredient_list_table.heading("Amount", text="Amount")
        self.ingredient_list_table.column("Amount", width=110, anchor=CENTER)
        self.style.configure("Custom.Treeview", rowheight=22)
        self.style.configure("Custom.Treeview.Heading", foreground='orange', font=(default, 10))
        self.ingredient_list_table.grid(column=4, row=0, rowspan=3, padx=(10, 5), pady=(5, 0), sticky=W)
        self.ingredient_list_table.bind('<<TreeviewSelect>>', self.ingredient_row_select)
        self.ingredient_list_table['displaycolumns'] = ("Ingredient Name","Amount")
        self.ingredient_list_table.config(style='Custom.Treeview')

        # Interface for Instructions Frame's Widgets
        self.instructions_frame = ttkb.LabelFrame(self.add_new_frame, text="Cooking Instructions", style="warning",
                                                  height=75, borderwidth=20, labelanchor="n", )
        self.instructions_frame.grid(row=0, column=2, padx=(20, 10), pady=(15, 0), sticky=W, rowspan=2)
        self.instructions_text = Text(self.instructions_frame, height=36, width=45, wrap=WORD, )
        self.instructions_text.pack()

        self.add_new_recipe_button = ttkb.Button(self.add_new_frame, text="Add New Recipe", style="info,outline",
                                                 width=113, command=self.general_data_validate)
        self.add_new_recipe_button.grid(row=2, column=0, pady=(30, 20), ipady=10)

        self.amend_exist_recipe_button = ttkb.Button(self.add_new_frame, text="Amend Exist Recipe",
                                                     style="info,outline", width=50,
                                                     command=lambda: self.switch_between_frames(frame_index=1))
        self.amend_exist_recipe_button.grid(row=2, column=2, pady=(30, 20), ipady=10, padx=(8, 0))

        """
            Loading Widgets within Amend Frame
        """
        self.amend_result_show_index: int = 0
        self.amend_recipe_search_frame = ttkb.LabelFrame(self.amend_exist_frame, text="Search Recipe",
                                                   style="warning", height=70, borderwidth=20, labelanchor="n", )
        self.amend_recipe_search_frame.grid(row=0, column=0, columnspan=3, padx=(10, 10), pady=(15, 0), sticky=W, )
        self.amend_recipe_search_entry = ttkb.Entry(self.amend_recipe_search_frame, justify='center', width=120, style='info')
        self.amend_recipe_search_entry.grid(row=0, column=0, padx=5, pady=5)
        self.amend_recipe_search_entry.focus()
        self.amend_recipe_search_entry.bind('<Return>', self.__amend_recipes_search_results)
        self.amend_recipe_search_button = ttkb.Button(self.amend_recipe_search_frame, text="Get Result", style='info', command=self.__amend_recipes_search_results)
        self.amend_recipe_search_button.grid(row=0, column=1, padx=5, pady=5, ipadx=20, )
        self.amend_recipe_search_next_button = ttkb.Button(self.amend_recipe_search_frame, text="Next Result", style='info', command=self.amend_load_search_result)
        self.amend_recipe_search_next_button.grid(row=0, column=2, padx=5, pady=5, ipadx=20, )
        self.amend_recipe_search_next_button.config(state=tk.DISABLED)




        self.amend_general_info_frame = ttkb.LabelFrame(self.amend_exist_frame, text="Recipe's General Info",
                                                        style="info", height=70, borderwidth=20, labelanchor="n", )
        self.amend_general_info_frame.grid(row=1, column=0, padx=(10, 10), pady=(15, 0), sticky=W, )
        self.amend_title_label = ttkb.Label(self.amend_general_info_frame, text="Recipe Name :")
        self.amend_title_label.grid(column=0, row=0, padx=(5, 0), pady=10, sticky='w')
        self.amend_title_entry = ttkb.Entry(self.amend_general_info_frame, width=30, style="success")
        self.amend_title_entry.grid(column=1, row=0, padx=(5, 5), pady=10, columnspan=2, sticky='w')
        self.amend_serving_type_label = ttkb.Label(self.amend_general_info_frame, text="Serving Type :")
        self.amend_serving_type_label.grid(column=0, row=1, padx=5, pady=10, sticky='w')
        self.amend_serving_type_combo = ttkb.Combobox(self.amend_general_info_frame, values=RecipeManagement.SERVING_TYPE,
                                                      style="success", width=28, justify="center", state="readonly")
        self.amend_serving_type_combo.current(2)
        self.amend_serving_type_combo.grid(column=1, row=1, padx=5, pady=10, columnspan=2, sticky='w')
        self.amend_halal_food_label = ttkb.Label(self.amend_general_info_frame, text="Is This Halal Food   :")
        self.amend_halal_food_label.grid(column=0, row=2, padx=(7, 15), pady=10, sticky='w')
        self.amend_halal_yes_radiobutton = ttkb.Radiobutton(self.amend_general_info_frame, style="success", text="Yes",
                                                      value=1, variable=self.selected_value)
        self.amend_halal_yes_radiobutton.grid(column=1, row=2, padx=10, pady=10, sticky='w')
        self.amend_halal_no_radiobutton = ttkb.Radiobutton(self.amend_general_info_frame, style="danger", text="No", value=0,
                                                     variable=self.selected_value)
        self.amend_halal_no_radiobutton.grid(column=2, row=2, padx=0, pady=10, sticky='w')
        self.amend_category_label = ttkb.Label(self.amend_general_info_frame, text="Diet Category :")
        self.amend_category_label.grid(column=0, row=3, padx=5, pady=10, sticky='w')
        self.amend_diet_category_combo = ttkb.Combobox(self.amend_general_info_frame, values=RecipeManagement.DIET_CATEGORY,
                                                       style="success", width=28, justify="center", state="readonly")
        self.amend_diet_category_combo.current(0)
        self.amend_diet_category_combo.grid(column=1, row=3, padx=5, pady=10, columnspan=2,sticky='w')

        self.amend_cooking_time_label = ttkb.Label(self.amend_general_info_frame, text="Cooking Time :")
        self.amend_cooking_time_label.grid(column=0, row=4, padx=(7, 15), pady=10, sticky='w')
        self.amend_cooking_time_entry = ttkb.Entry(self.amend_general_info_frame, style="success", width=20, justify="center",)
        self.amend_cooking_time_entry.grid(column=1, row=4, padx=(5, 5), pady=10, sticky='w')
        self.amend_cooking_time_minutes_label = ttkb.Label(self.amend_general_info_frame, text="Minutes")
        self.amend_cooking_time_minutes_label.grid(column=2, row=4, padx=(7, 15), pady=10, sticky='w')

        self.amend_calories_label = ttkb.Label(self.amend_general_info_frame, text="Calories Per Serving :")
        self.amend_calories_label.grid(column=0, row=5, padx=(7, 15), pady=10, sticky='w')
        self.amend_calories_entry = ttkb.Entry(self.amend_general_info_frame, width=30, style="success", justify="center")
        self.amend_calories_entry.grid(column=1, row=5, padx=(5, 5), pady=10, columnspan=2, sticky='w')

        self.amend_recipe_picture_one_label = ttkb.Label(self.amend_general_info_frame, text="Image One  :")
        self.amend_recipe_picture_one_label.grid(column=0, row=6, padx=(7, 15), pady=10, sticky='w')
        self.amend_recipe_picture_one_entry = ttkb.Entry(self.amend_general_info_frame, width=20, style="success")
        self.amend_recipe_picture_one_entry.grid(column=1, row=6, pady=10, padx=(5, 0), sticky='w',)
        self.amend_recipe_picture_one_entry.bind('<Double-Button-1>', self.amend_show_image_one)
        self.amend_recipe_picture_one_button = ttkb.Button(self.amend_general_info_frame, text="Change",
                                                           style="success",command=lambda: self.get_file_directory('one','amend'))
        self.amend_recipe_picture_one_button.grid(column=2, row=6, pady=10, padx=(5, 0), sticky='w')

        self.amend_recipe_picture_two_label = ttkb.Label(self.amend_general_info_frame, text="Image Two  :")
        self.amend_recipe_picture_two_label.grid(column=0, row=7, padx=(7, 15), pady=10, sticky='w')
        self.amend_recipe_picture_two_entry = ttkb.Entry(self.amend_general_info_frame, width=20, style="success")
        self.amend_recipe_picture_two_entry.grid(column=1, row=7, pady=10, padx=(5, 0), sticky='w')
        self.amend_recipe_picture_two_entry.bind('<Double-Button-1>', self.amend_show_image_two)
        self.amend_recipe_picture_two_button = ttkb.Button(self.amend_general_info_frame,text="Change",style="success",command=lambda: self.get_file_directory('two','amend') )
        self.amend_recipe_picture_two_button.grid(column=2, row=7, pady=10, padx=(5, 0), sticky='w')


        self.amend_recipe_picture_three_label = ttkb.Label(self.amend_general_info_frame, text="Image Three :")
        self.amend_recipe_picture_three_label.grid(column=0, row=8, padx=(7, 15), pady=10, sticky='w')
        self.amend_recipe_picture_three_entry = ttkb.Entry(self.amend_general_info_frame, width=20, style="success")
        self.amend_recipe_picture_three_entry.grid(column=1, row=8, pady=10, padx=(5, 0), sticky='w',)
        self.amend_recipe_picture_three_entry.bind('<Double-Button-1>', self.amend_show_image_three)
        self.amend_recipe_picture_three_button = ttkb.Button(self.amend_general_info_frame, text="Change",
                                                           style="success",command=lambda: self.get_file_directory('three','amend'))
        self.amend_recipe_picture_three_button.grid(column=2, row=8, pady=10, padx=(5, 0), sticky='w')

        # Amend Frame middle sub-frame 'Ingredient List'
        self.amend_ingredient_list_frame = ttkb.LabelFrame(self.amend_exist_frame, text="Ingredient List",
                                                           style="danger", height=70, borderwidth=20,
                                                           labelanchor="n", )
        self.amend_ingredient_list_frame.grid(row=1, column=1, padx=(20, 10), pady=(15, 0), sticky=W, )
        self.amend_ingredient_list_table = ttkb.Treeview(self.amend_ingredient_list_frame, columns=RecipeManagement.COLUMNS,
                                                         show='headings', height=8)
        self.amend_ingredient_list_table.heading("Ingredient Name", text="Ingredient Name")
        self.amend_ingredient_list_table.column("Ingredient Name", width=120, anchor=CENTER)
        self.amend_ingredient_list_table.heading("Amount", text="Amount")
        self.amend_ingredient_list_table.column("Amount", width=100, anchor=CENTER)
        self.amend_ingredient_list_table.grid(column=0, row=0, padx=5, pady=(5, 10), columnspan=2, sticky='w', )
        self.amend_ingredient_list_table.config(style='Custom.Treeview')
        self.amend_ingredient_list_table['displaycolumns'] = ("Ingredient Name","Amount")
        self.amend_ingredient_list_table.bind('<<TreeviewSelect>>', self.amend_ingredient_display)

        self.amend_ingredient_name_label = ttkb.Label(self.amend_ingredient_list_frame, text="Name :")
        self.amend_ingredient_name_label.grid(column=0, row=1, padx=7, pady=6, sticky='w', )
        self.amend_ingredient_name_entry = ttkb.Entry(self.amend_ingredient_list_frame, width=19, style='primary',justify='center')
        self.amend_ingredient_name_entry.grid(column=1, row=1, padx=7, pady=6, sticky='w', columnspan=3)

        self.amend_ingredient_amount_label = ttkb.Label(self.amend_ingredient_list_frame, text="Amount :")
        self.amend_ingredient_amount_label.grid(column=0, row=2, padx=7, pady=6, sticky='w')
        self.amend_ingredient_amount_entry = ttkb.Entry(self.amend_ingredient_list_frame, width=19, style='primary',justify='center')
        self.amend_ingredient_amount_entry.grid(column=1, row=2, padx=7, pady=6, sticky='w')

        self.amend_ingredient_unit_label = ttkb.Label(self.amend_ingredient_list_frame, text="Unit :")
        self.amend_ingredient_unit_label.grid(column=0, row=3, padx=7, pady=6, sticky='w')
        self.amend_ingredient_unit_combo = ttkb.Combobox(self.amend_ingredient_list_frame, values=RecipeManagement.UNIT,
                                                         style="primary", width=17, justify="center", state="readonly")
        self.amend_ingredient_unit_combo.current(0)
        self.amend_ingredient_unit_combo.grid(column=1, row=3, padx=7, pady=6, sticky='w')

        self.amend_ingredient_type_label = ttkb.Label(self.amend_ingredient_list_frame, text="Type :")
        self.amend_ingredient_type_label.grid(column=0, row=4, padx=7, pady=6, sticky='w')
        self.amend_ingredient_type_combo = ttkb.Combobox(self.amend_ingredient_list_frame,
                                                         values=RecipeManagement.INGREDIENT_TYPE,
                                                         style="primary", width=17, justify="center", state="readonly")
        self.amend_ingredient_type_combo.current(0)
        self.amend_ingredient_type_combo.grid(column=1, row=4, padx=7, pady=6, sticky='w')

        self.amend_add_ingredient_button = ttkb.Button(self.amend_ingredient_list_frame, text="Add",
                                                       style="outline", width=6, state=tk.DISABLED,
                                                       command=self.amend_add_ingredient_listview)
        self.amend_add_ingredient_button.grid(row=5, column=0,pady=(9, 0), sticky='w', )
        self.amend_update_ingredient_button = ttkb.Button(self.amend_ingredient_list_frame, text="Update",
                                                          style="outline", width=8, command=self.amend_update_ingredient_listview,
                                                          state=tk.DISABLED)
        self.amend_update_ingredient_button.grid(row=5, column=1,padx=(3,0),pady=(9, 0), sticky='w', )
        self.amend_delete_ingredient_button = ttkb.Button(self.amend_ingredient_list_frame, text="Delete",
                                                    style="outline", width=6, command=self.amend_delete_ingredient,
                                                    state=tk.DISABLED,)
        self.amend_delete_ingredient_button.grid(row=5, column=1, pady=(9, 0), sticky='e')


        self.amend_instructions_frame = ttkb.LabelFrame(self.amend_exist_frame, text="Cooking Instructions",
                                                        style="success", height=70, borderwidth=20, labelanchor="n", )
        self.amend_instructions_frame.grid(row=1, column=2, padx=(20, 10), pady=(15, 0), sticky=W, )
        self.amend_instructions_text = Text(self.amend_instructions_frame, height=27, width=41, wrap=WORD, )
        self.amend_instructions_text.pack(pady=3)

        self.amend_update_button = ttkb.Button(self.amend_exist_frame, text="Update Recipe", style="info,outline",
                                               width=59, state="disabled", command=self.amend_update_general_info)
        self.amend_update_button.grid(row=2, column=0, padx=(10, 0), pady=(40, 0), ipady=5, sticky='w')

        self.amend_delete_button = ttkb.Button(self.amend_exist_frame, text="Delete Recipe", style="info,outline",
                                               width=42, state="disabled", command=self.delete_recipe)
        self.amend_delete_button.grid(row=2, column=1, padx=(19, 0), pady=(40, 0), ipady=5, sticky='w')

        self.amend_add_new_frame_button = ttkb.Button(self.amend_exist_frame, text="Add New Recipe", style="info,outline",
                                                width=47, command=lambda: self.switch_between_frames(frame_index=0))
        self.amend_add_new_frame_button.grid(row=2, column=2, pady=(40, 0), padx=(5, 0), ipady=5)

    def general_data_validate(self) -> None:
        title_check: bool = False
        calories_field_check: bool = False
        viewtable_empty_check: bool = False
        image_one_check: bool = False
        image_two_check: bool = False
        image_three_check: bool = False
        if not InputValidate(self.title_entry.get()).check_text_only():
            Messagebox.show_error(parent=self.instructions_frame, title="Error Message",
                                  message="Please Input The Recipe Title Correctly !")
        else:
            title_check = True

        if not InputValidate(self.calories_entry.get()).check_number_only():
            Messagebox.show_error(parent=self.instructions_frame, title="Error Message",
                                  message="Please Input Calories Entry Correctly !")
        else:
            calories_field_check = True

        if len(self.ingredient_items_list) == 0:
            Messagebox.show_error(parent=self.instructions_frame, title="Error Message",
                                  message="Please Add Ingredient To Table !")
        else:
            viewtable_empty_check = True

        if  (not InputValidate(self.recipe_picture_one_entry.get().strip()).check_picture()
                or not InputValidate(self.recipe_picture_two_entry.get().strip()).check_picture() or
                not InputValidate(self.recipe_picture_three_entry.get().strip()).check_picture()):
            Messagebox.show_error(parent=self.instructions_frame, title="Error Message",
                                  message="Please Add Recipe Pictures Correctly !")
        else:
            image_one_check = True
            image_two_check = True
            image_three_check = True

        if (title_check and calories_field_check and viewtable_empty_check and image_one_check
                and image_two_check and image_three_check):
            self.insert_new_recipe()

    def ingredient_data_validate(self) -> None:
        ingredient_name_check: bool = False
        ingredient_amount_check: bool = False
        ingredient_exist: bool = False
        if not InputValidate(self.ingredient_name_entry.get()).check_text_only() or len(
                self.ingredient_name_entry.get().strip()) == 0:
            Messagebox.show_error(parent=self.instructions_frame, title="Error Message",
                                  message="Please Input Ingredient Name Correctly !")
        else:
            ingredient_name_check = True

        if '.' in self.ingredient_amount_entry.get().strip():
            Messagebox.show_error(parent=self.instructions_frame, title="Error Message",
                                  message="Please Input Amount By Using Whole Number !")
        elif not InputValidate(self.ingredient_amount_entry.get().strip()).check_number_only() or len(
                self.ingredient_amount_entry.get().strip()) == 0:
            Messagebox.show_error(parent=self.instructions_frame, title="Error Message",
                                  message="Please Input Ingredient Amount Correctly !")
        else:
            ingredient_amount_check = True

        if ingredient_name_check and ingredient_amount_check:
            for each_ingredient in self.ingredient_items_list:
                if self.ingredient_name_entry.get().strip() in each_ingredient:
                    Messagebox.show_error(parent=self.instructions_frame, title="Error Message",
                                          message="Please Do Not Add Duplicated Ingredient !")
                    ingredient_exist = True
                    break
            if not ingredient_exist:
                self.ingredient_items_list.append([self.ingredient_name_entry.get().lower().strip(),
                                                   self.ingredient_amount_entry.get().strip(),
                                                   self.ingredient_unit_combo.get(),
                                                   self.ingredient_type_combo.get()], )
                self.ingredient_list_table.insert(parent='', index='end',
                                                  values=[self.ingredient_name_entry.get().strip(),
                                                          self.ingredient_amount_entry.get().strip()
                                                          + ' ' +
                                                          self.ingredient_unit_combo.get(), ])
                self.ingredient_name_entry.delete(0, END)
                self.ingredient_amount_entry.delete(0, END)
                self.delete_ingredient_button.config(state=tk.NORMAL)

    def insert_new_recipe(self) -> None:
        # Check if there is duplicate recipe
        duplicate_recipe_search = f"SELECT * FROM recipes WHERE recipe_name == ?"
        duplicate_check_result: list = ConnectDatabase(duplicate_recipe_search).execute_sql_with_values((self.title_entry.get(),))
        recipe_category: str = "desserts"
        vegan_or_not: bool = True
        # find out what recipe category is
        for each_ingredient in self.ingredient_items_list:
            if 'rice' in  each_ingredient[0].lower():
                recipe_category = "rice and noodles dish"
                break
            elif 'noodle' in  each_ingredient[0].lower():
                recipe_category = "rice and noodles dish"
                break

            match each_ingredient[3].lower():
                case 'meat':
                        recipe_category = "meaty one"
                        break
                case 'fish':
                        recipe_category = "seafood and shellfish"
                        break
                case 'seafood and shellfish':
                        recipe_category = "seafood and shellfish"
                        break

        if recipe_category == "rice and noodles dish":
            for each_ingredient in self.ingredient_items_list:
                if (each_ingredient[3].lower() == "egg" or each_ingredient[3].lower() == "dairy product"
                        or each_ingredient[3].lower() == "fish" or each_ingredient[3].lower() == "seafood and shellfish"
                        or each_ingredient[3].lower() == "meat"):
                    vegan_or_not = False
                    break
            if vegan_or_not:
                recipe_category = "vegan"

        if recipe_category == "desserts":
            for each_ingredient in self.ingredient_items_list:
                if each_ingredient[3].lower() == "egg" or each_ingredient[3].lower() == "dairy product":
                    vegan_or_not = False
                    break
            if vegan_or_not:
                recipe_category = "vegan"

        if len(duplicate_check_result) == 0:
            # After Checking if recipe exist, insert data into Recipe table with corresponding category and serving type

            picture_one:str = ""
            picture_two: str = ""
            picture_three: str = ""
            category_search: str = f"SELECT category_id FROM category WHERE category_name == ?"
            category_result: list = ConnectDatabase(category_search).execute_sql_with_values((self.diet_category_combo.get(),))

            serving_type_search: str = f"SELECT dish_id FROM dish WHERE dish_type == ?"
            serving_type_result: list = ConnectDatabase(serving_type_search).execute_sql_with_values(
                (self.serving_type_combo.get(),))

            # create a new directory with named with recipe title, copy three recipe images into this folder
            recipe_name: str = self.title_entry.get().lower()
            parent_dir = "Images/"
            dir_name: str = "_".join(recipe_name.split(" "))
            path = os.path.join(parent_dir, dir_name)

            try:
                os.makedirs(path)
            except OSError:
                print(f"Creation of the directory {path} failed")

            try:
                shutil.copy(src=self.recipe_picture_one_entry.get().lower().strip(), dst=f"{path}/{dir_name}_one.jpg")
                shutil.copy(src=self.recipe_picture_two_entry.get().lower().strip(), dst=f"{path}/{dir_name}_two.jpg")
                shutil.copy(src=self.recipe_picture_three_entry.get().lower().strip(),
                            dst=f"{path}/{dir_name}_three.jpg")
                picture_one = f"{path}/{dir_name}_one.jpg"
                picture_two = f"{path}/{dir_name}_two.jpg"
                picture_three = f"{path}/{dir_name}_three.jpg"
            except OSError:
                print("can't copy the file")

            insert_recipes_values: tuple = (
                self.title_entry.get().strip(), category_result[0][0], self.instructions_text.get("1.0", END),
                picture_one,picture_two,picture_three,self.cooking_time_entry.get() ,serving_type_result[0][0],self.calories_entry.get().strip(),
                self.selected_value.get(), recipe_category)
            insert_recipes_str: str = (
                f"INSERT INTO recipes(recipe_name,category_id,instructions,image_one,image_two,image_three,"
                f"cooking_time,dish_id,calories_per_serving,is_halal_food, recipe_category) VALUES(?,?,?,?,?,?,?,?,?,?,?)")
            ConnectDatabase(insert_recipes_str).execute_insert_query(insert_recipes_values)

            # Insert data into Ingredient table with corresponding
            for each_ingredient in self.ingredient_items_list:
                ingredient_search: str = f"SELECT * FROM ingredient WHERE ingredient_name == ?"
                ingredient_result: list = ConnectDatabase(ingredient_search).execute_sql_with_values((each_ingredient[0],))
                if len(ingredient_result) == 0:
                    ingredient_type_id_sql = "select type_id from food_type_list where type_name=?"
                    ingredient_type_id = ConnectDatabase(ingredient_type_id_sql).execute_sql_with_values((each_ingredient[3],))
                    insert_recipe_ingredient_str: str = (
                        f"INSERT INTO ingredient(ingredient_name,ingredient_type) VALUES(?,?)")
                    insert_ingredient_values = (each_ingredient[0], ingredient_type_id[0][0])
                    ConnectDatabase(insert_recipe_ingredient_str).execute_insert_query(insert_ingredient_values)
                    ingredient_result: list = ConnectDatabase(ingredient_search).execute_sql_with_values((each_ingredient[0],))

                # Insert data into Recipe Ingredient table with corresponding Recipe ID, Ingredient ID and Unit ID
                recipe_id_search: str = f"SELECT recipe_id FROM recipes WHERE recipes.recipe_name == ?"
                recipe_id_result: list = ConnectDatabase(recipe_id_search).execute_sql_with_values((self.title_entry.get().strip(),))

                unit_search: str = f"SELECT unit_id FROM unit WHERE unit_name == ?"
                unit_result: list = ConnectDatabase(unit_search).execute_sql_with_values((each_ingredient[2],))
                insert_recipe_ingredient_values: tuple = (
                    recipe_id_result[0][0], ingredient_result[0][0], each_ingredient[1], unit_result[0][0])
                insert_recipe_ingredient_str: str = (
                    f"INSERT INTO recipe_ingredient(recipe_id,ingredient_id,amount,unit) VALUES(?,?,?,?)")
                ConnectDatabase(insert_recipe_ingredient_str).execute_insert_query(insert_recipe_ingredient_values)

            self.ingredient_items_list.clear()
            self.title_entry.delete(0, END)
            self.recipe_picture_one_entry.delete(0, END)
            self.recipe_picture_two_entry.delete(0, END)
            self.recipe_picture_three_entry.delete(0, END)
            self.cooking_time_entry.delete(0, END)
            self.calories_entry.delete(0, END)
            self.instructions_text.delete('1.0', END)
            for each_row in self.ingredient_list_table.get_children():
                self.ingredient_list_table.delete(each_row)
            Messagebox.show_info(parent=self.instructions_frame, title="Confirmation Message",
                                 message="The New Recipe Has Been Added Successfully")

        else:
            Messagebox.show_error(parent=self.instructions_frame, title="Error Message",
                                  message="Recipe Exists, You Can Amend it By Click 'Amend Exist Recipe' !")

    def get_file_directory(self, entry_number,frame_name) -> None:
        path: str = tkinter.filedialog.askopenfilename(parent=self, initialdir="C:/",
                                                       filetypes=(("PNG Files", "*.png"),
                                                                  ("JPEG Files", "*.jpeg"),
                                                                  ("JPG Files", "*.jpg"),
                                                                  ("GIF Files", "*.gif"),
                                                                  ("WEBP files", "*.webp")))
        if path:
            if frame_name=='add':
                match entry_number:
                    case 'one':
                        self.recipe_picture_one_entry.delete(0,END)
                        self.recipe_picture_one_entry.insert(0, path)
                    case 'two':
                        self.recipe_picture_two_entry.delete(0, END)
                        self.recipe_picture_two_entry.insert(0, path)
                    case 'three':
                        self.recipe_picture_three_entry.delete(0, END)
                        self.recipe_picture_three_entry.insert(0, path)
            elif frame_name=='amend':
                match entry_number:
                    case 'one':
                        self.amend_recipe_picture_one_entry.delete(0,END)
                        self.amend_recipe_picture_one_entry.insert(0, path)
                    case 'two':
                        self.amend_recipe_picture_two_entry.delete(0, END)
                        self.amend_recipe_picture_two_entry.insert(0, path)
                    case 'three':
                        self.amend_recipe_picture_three_entry.delete(0, END)
                        self.amend_recipe_picture_three_entry.insert(0, path)

    def ingredient_row_select(self, even):
        pass

    def ingredient_table_row_delete(self):
        print(self.ingredient_items_list)
        if not len(self.ingredient_list_table.get_children()) == 0:
            if not len(self.ingredient_list_table.selection()) == 0:
                self.ingredient_table_iid_number = self.ingredient_list_table.selection()[0]
                row_info = self.ingredient_list_table.item(self.ingredient_list_table.selection()[0])['values']
                for each_row in self.ingredient_items_list:
                    if each_row[0] == row_info[0]:
                        self.ingredient_items_list.remove(each_row)
                print(self.ingredient_items_list)
                self.ingredient_list_table.delete(self.ingredient_table_iid_number)
                if len(self.ingredient_list_table.get_children()) == 0:
                    self.delete_ingredient_button.state(['disabled'])

    # Below are functions for Amend Recipe
    def __amend_recipes_search_results(self,event = None):
        self.result_index = 0
        self.keyword_search_result:list =[]
        load_all_recipes_sql: str = (
            f"SELECT recipes.recipe_id, recipes.recipe_name,recipes.cooking_time,recipes.calories_per_serving,recipes.is_halal_food,"
            f"c.category_name,d.dish_type,recipes.image_one,recipes.image_two,recipes.image_three,recipes.instructions FROM recipes INNER JOIN category c "
            f"on c.category_id = recipes.category_id INNER JOIN dish d "
            f"on d.dish_id = recipes.dish_id where recipes.recipe_name LIKE ?")
        self.keyword_search_result = ConnectDatabase(load_all_recipes_sql).execute_sql_with_values(
            ('%' + self.amend_recipe_search_entry.get().strip() + '%',))
        if len(self.keyword_search_result) != 0:
            self.amend_load_search_result()
            if len(self.keyword_search_result) > 1:
                self.amend_recipe_search_next_button.config(state='normal')
            else:
                self.amend_recipe_search_next_button.config(state='disabled')
            self.amend_update_button.config(state='normal')
            self.amend_delete_button.config(state='normal')
        else:
            Messagebox.show_info(parent=self.amend_ingredient_list_frame, title='No Result Found',
                                 message="Sorry,There is no recipe match your search !", )


    def amend_load_search_result(self):
        self.amend_clear_frame()
        self.current_recipe_id = self.keyword_search_result[self.result_index][0]
        self.amend_title_entry.insert(END, self.keyword_search_result[self.result_index][1].title())
        if self.keyword_search_result[self.result_index][4] == 0:
            self.selected_value.set('0')
        else:
            self.selected_value.set('1')
        match self.keyword_search_result[self.result_index][6].lower():
            case 'dinner':
                self.amend_serving_type_combo.current(2)
            case 'lunch':
                self.amend_serving_type_combo.current(1)
            case 'breakfast':
                self.amend_serving_type_combo.current(0)
        match self.keyword_search_result[self.result_index][5].lower():
            case 'flexitarian (normal diet)':
                self.amend_diet_category_combo.current(0)
            case 'vegan':
                self.amend_diet_category_combo.current(1)

        self.amend_cooking_time_entry.insert(END, self.keyword_search_result[self.result_index][2].split(" ")[0])
        self.amend_calories_entry.insert(END, self.keyword_search_result[self.result_index][3])
        self.amend_recipe_picture_one_entry.insert(END, self.keyword_search_result[self.result_index][7])
        self.amend_recipe_picture_two_entry.insert(END, self.keyword_search_result[self.result_index][8])
        self.amend_recipe_picture_three_entry.insert(END, self.keyword_search_result[self.result_index][9])
        self.amend_instructions_text.insert(END, self.keyword_search_result[self.result_index][10])

        load_all_ingredient_sql: str = ("SELECT i.ingredient_name, recipe_ingredient.amount,u.unit_name, i.ingredient_type from "
                                        "recipe_ingredient inner join ingredient i on "
                                        "recipe_ingredient.ingredient_id = i.ingredient_id inner join unit u on "
                                        "recipe_ingredient.unit = u.unit_id where recipe_ingredient.recipe_id = ?")
        ingredient_search_result_list = ConnectDatabase(load_all_ingredient_sql).execute_sql_with_values(
            (self.keyword_search_result[self.result_index][0],))
        for each_ingredient in ingredient_search_result_list:
            self.amend_ingredient_list_table.insert("", END, values=(
                each_ingredient[0].title(), str(each_ingredient[1]) + " " + each_ingredient[2],each_ingredient[3]))
        self.result_index += 1
        self.amend_add_ingredient_button.config(state='normal')
        if self.result_index == len(self.keyword_search_result):
            self.result_index = 0


    def amend_ingredient_display(self,event):
        if len(self.amend_ingredient_list_table.selection()) > 0 :
            self.amend_ingredient_name_entry.delete(0, END)
            self.amend_ingredient_amount_entry.delete(0, END)
            self.amend_delete_ingredient_button.config(state='normal')
            self.amend_update_ingredient_button.config(state='normal')
            row_id: str = self.amend_ingredient_list_table.selection()[0]
            row_value = self.amend_ingredient_list_table.item(row_id)['values']
            self.amend_ingredient_name_entry.insert(END, row_value[0])
            self.amend_ingredient_amount_entry.insert(END, row_value[1].split(" ")[0])
            index_of_unit = RecipeManagement.UNIT.index(row_value[1].split(" ")[1])
            self.amend_ingredient_unit_combo.current(index_of_unit)
            ingredient_type_name_sql = ("select f.type_name from ingredient inner join food_type_list f on ingredient.ingredient_type=f.type_id "
                                    "where ingredient.ingredient_name = ?")
            ingredient_type_name = ConnectDatabase(ingredient_type_name_sql).execute_sql_with_values((row_value[0].lower(),))

            index_of_ingredient_type = RecipeManagement.INGREDIENT_TYPE.index(ingredient_type_name[0][0])
            self.amend_ingredient_type_combo.current(index_of_ingredient_type)

    def amend_update_ingredient_listview(self):
        if len(self.amend_ingredient_list_table.selection()) > 0:
            current_row = self.amend_ingredient_list_table.selection()[0]
            ingredient_name = self.amend_ingredient_name_entry.get().strip()
            ingredient_amount = self.amend_ingredient_amount_entry.get().strip()
            ingredient_unit = self.amend_ingredient_unit_combo.get()
            food_type_id_sql = "select type_id from food_type_list where type_name=?"
            ingredient_food_type_id = ConnectDatabase(food_type_id_sql).execute_sql_with_values((self.amend_ingredient_type_combo.get(),))
            self.amend_ingredient_list_table.item(current_row,values=(ingredient_name.title(),ingredient_amount+ " " + ingredient_unit,ingredient_food_type_id[0][0]))
            ingredient_exist_not_sql = 'select ingredient_id from ingredient where ingredient_name = ?'
            ingredient_exist_not = ConnectDatabase(ingredient_exist_not_sql).execute_sql_with_values((ingredient_name.lower(),))
            if len(ingredient_exist_not) == 0:
                insert_new_ingredient_sql = "insert into ingredient(ingredient_name,ingredient_type) values (?,?)"
                ConnectDatabase(insert_new_ingredient_sql).execute_insert_query((ingredient_name.lower(), ingredient_food_type_id[0][0]))
            Messagebox.show_info(parent=self.amend_ingredient_list_frame, title='Operation Successful',
                                  message="The ingredient information has been updated !")
            self.amend_ingredient_list_table.selection_remove(current_row)
            self.amend_ingredient_name_entry.delete(0, END)
            self.amend_ingredient_amount_entry.delete(0, END)
        else:
            Messagebox.show_error(parent=self.amend_ingredient_list_frame, title='Operation Errors',
                                  message="Please select the ingredient you want to updated first !")

    def amend_add_ingredient_listview(self):
        ingredient_name = self.amend_ingredient_name_entry.get().strip()
        ingredient_amount = self.amend_ingredient_amount_entry.get().strip()
        if InputValidate(ingredient_name).check_text_only() and InputValidate(ingredient_amount).check_number_only() :
            ingredient_unit = self.amend_ingredient_unit_combo.get()
            ingredient_type_id_sql = "select type_id from food_type_list where type_name=?"
            ingredient_type_id = ConnectDatabase(ingredient_type_id_sql).execute_sql_with_values((self.amend_ingredient_type_combo.get(),))[0][0]
            self.amend_ingredient_list_table.insert(parent="",index= END,values=(ingredient_name.title(),ingredient_amount+ " " + ingredient_unit,ingredient_type_id))
            ingredient_exist_not_sql = 'select ingredient_id from ingredient where ingredient_name = ?'
            ingredient_exist_not = ConnectDatabase(ingredient_exist_not_sql).execute_sql_with_values((ingredient_name,))
            if len(ingredient_exist_not) == 0:
                insert_new_ingredient_sql = "insert into ingredient(ingredient_name,ingredient_type) values (?,?)"
                ConnectDatabase(insert_new_ingredient_sql).execute_insert_query((ingredient_name,ingredient_type_id))
            self.amend_ingredient_type_combo.current(0)
            self.amend_ingredient_unit_combo.current(0)
            self.amend_ingredient_name_entry.delete(0, END)
            self.amend_ingredient_amount_entry.delete(0, END)
        else:
            Messagebox.show_error(parent=self.amend_ingredient_list_frame,title='Input Errors',message="Please input ingredient name and amount correctly !")


    def switch_between_frames(self, frame_index):
        if frame_index == 0:
            self.amend_exist_frame.forget()
            self.add_new_frame.pack(fill=BOTH, expand=YES)
        else:
            self.add_new_frame.forget()
            self.amend_exist_frame.pack(fill=BOTH, expand=YES)

    def close_window(self):
        self.destroy()
        self.parent.deiconify()
        self.parent.username_entry.focus()

    def amend_clear_frame(self):
        self.amend_title_entry.delete(0, END)
        self.amend_cooking_time_entry.delete(0, END)
        self.amend_calories_entry.delete(0, END)
        self.amend_recipe_picture_one_entry.delete(0, END)
        self.amend_recipe_picture_two_entry.delete(0, END)
        self.amend_recipe_picture_three_entry.delete(0, END)
        self.amend_instructions_text.delete(1.0, index2=END)
        self.amend_ingredient_name_entry.delete(0, END)
        self.amend_ingredient_amount_entry.delete(0, END)
        self.amend_recipe_search_entry.delete(0, END)
        for each_ingredient in self.amend_ingredient_list_table.get_children():
            self.amend_ingredient_list_table.delete(each_ingredient)
        if self.current_recipe_id == -1 :
            self.amend_update_button.config(state='disabled')
            self.amend_delete_button.config(state='disabled')
            self.amend_recipe_search_next_button.config(state='disabled')
        self.amend_recipe_search_entry.focus()

    def amend_show_image_one(self,event):
        if self.current_recipe_id != -1 :
            try:
                Image.open(self.amend_recipe_picture_one_entry.get())
                ImageReview(self,self.amend_recipe_picture_one_entry.get())
            except FileNotFoundError:
                Messagebox.show_error(parent=self.amend_ingredient_list_frame, title="File Not Found Error",
                                      message="Can't Find The Image, Please Make Sure The Path Is Right !")

    def amend_show_image_two(self,event):
        if self.current_recipe_id != -1:
            try:
                Image.open(self.amend_recipe_picture_two_entry.get())
                ImageReview(self, self.amend_recipe_picture_two_entry.get())
            except FileNotFoundError:
                Messagebox.show_error(parent=self.amend_ingredient_list_frame, title="File Not Found Error",
                                      message="Can't Find The Image, Please Make Sure The Path Is Right !")

    def amend_show_image_three(self,event):
        if self.current_recipe_id != -1:
            try:
                Image.open(self.amend_recipe_picture_three_entry.get())
                ImageReview(self, self.amend_recipe_picture_three_entry.get())
            except FileNotFoundError:
                Messagebox.show_error(parent=self.amend_ingredient_list_frame, title="File Not Found Error",
                                      message="Can't Find The Image, Please Make Sure The Path Is Right !")


    def amend_delete_ingredient(self):
        row_id = self.amend_ingredient_list_table.selection()
        if  len(row_id) > 0:
            self.amend_ingredient_list_table.delete(row_id[0])
            self.amend_ingredient_name_entry.delete(0, END)
            self.amend_ingredient_amount_entry.delete(0, END)
        else:
            Messagebox.show_error(parent=self.amend_ingredient_list_frame, title="Operation Errors",message="Please select the row you want to delete!")

    def delete_recipe(self):
        user_confirmation = Messagebox.yesno(parent=self.amend_ingredient_list_frame,title="User Confirmation",message="Are You Sure To Delete The Recipe?")
        if user_confirmation == 'Yes':
            recipe_name_sql:str ='select recipe_name from recipes where recipe_id=?'
            recipe_name:str = ConnectDatabase(recipe_name_sql).execute_sql_with_values((self.current_recipe_id,))[0][0].lower()
            recipe_name = recipe_name.replace(' ','_')
            print(recipe_name)
        delete_recipe_sql: str = "Delete from recipes where recipe_id = ?"
        delete_recipe_ingredient_sql = "Delete from recipe_ingredient where recipe_id = ?"
        ConnectDatabase(delete_recipe_sql).execute_delete_query((self.current_recipe_id,))
        ConnectDatabase(delete_recipe_ingredient_sql).execute_delete_query((self.current_recipe_id,))
        try:
            shutil.rmtree(path="Images/{d}")
            self.amend_clear_frame()
            Messagebox.show_info(parent=self.amend_ingredient_list_frame, title="Recipe Deleted",
                                 message="The Recipe Has Been Deleted Success?")
        except FileNotFoundError:
            Messagebox.show_error(parent=self.amend_ingredient_list_frame, title="File Operation Error",
                                  message="Can't Find Recipe's Image Folder!")
        except NotADirectoryError:
            Messagebox.show_error(parent=self.amend_ingredient_list_frame, title="File Operation Error",
                                  message="Can't Find Recipe's Image Folder!")
        except OSError:
            Messagebox.show_error(parent=self.amend_ingredient_list_frame, title="File Operation Error",
                                  message="Can't Find Recipe's Image Folder!")




    def amend_update_general_info(self):
        if self.amend_data_validation():
            search_dish_id_sql = 'select dish_id from dish where dish_type = ?'
            dish_id = ConnectDatabase(search_dish_id_sql).execute_sql_with_values((self.amend_serving_type_combo.get(),))
            is_hala_food = self.selected_value.get()
            recipe_images_dir_sql: str = 'select image_one,image_two,image_three from recipes where recipe_id=?'
            recipe_images = ConnectDatabase(recipe_images_dir_sql).execute_sql_with_values((self.current_recipe_id,))
            image_one_slash_index = recipe_images[0][0].rindex("/")
            image_two_slash_index = recipe_images[0][1].rindex("/")
            image_three_slash_index = recipe_images[0][2].rindex("/")
            image_one_file_name = recipe_images[0][0][image_one_slash_index + 1:]
            image_two_file_name = recipe_images[0][1][image_two_slash_index + 1:]
            image_three_file_name = recipe_images[0][2][image_three_slash_index + 1:]
            recipe_name: str = "_".join(self.amend_title_entry.get().strip().lower().split(" "))
            parent_dir = "Images/"
            dir_name: str = "_".join(recipe_name.split(" ")) + "/"
            base_path = os.path.join(parent_dir, dir_name)
            if (self.amend_recipe_picture_one_entry.get().strip()[0:6] == "Images" and
                    self.amend_recipe_picture_two_entry.get().strip()[0:6] == "Images" and
                    self.amend_recipe_picture_three_entry.get().strip()[0:6]== "Images"):

                current_images_folder_slash_index = recipe_images[0][0].rindex("/")
                current_images_folder_name = recipe_images[0][0][7:current_images_folder_slash_index]
                print(recipe_images[0][0])
                print(current_images_folder_slash_index)
                print(base_path)
                try:
                    os.rename(f"Images/{current_images_folder_name}", f"Images/{recipe_name}")
                    image_one_new_path = base_path + image_one_file_name
                    image_two_new_path = base_path + image_two_file_name
                    image_three_new_path = base_path + image_three_file_name
                    search_diet_type_sql = 'select category_id from category where category_name = ?'
                    category_id = ConnectDatabase(search_diet_type_sql).execute_sql_with_values(
                        (self.amend_diet_category_combo.get(),))
                    update_general_info_sql = (
                        'Update recipes set recipe_name=?,instructions=?,image_one=?,image_two=?,image_three=?,'
                        'cooking_time=?,calories_per_serving=?,dish_id=?,is_halal_food=?,category_id=? where recipe_id = ?')
                    updated_values = (
                    self.amend_title_entry.get().strip(), self.amend_instructions_text.get('1.0', END).strip(),
                    image_one_new_path, image_two_new_path, image_three_new_path,
                    self.amend_cooking_time_entry.get().strip(),
                    self.amend_calories_entry.get().strip(), dish_id[0][0], is_hala_food, category_id[0][0],
                    self.current_recipe_id)
                    ConnectDatabase(update_general_info_sql).execute_update_query(updated_values)
                    self.amend_update_ingredient_list()
                    Messagebox.show_info(parent=self.amend_ingredient_list_frame, title='Information',
                                         message="Recipe Updated Successfully")
                except NotADirectoryError:
                    Messagebox.show_error(parent=self.amend_ingredient_list_frame, title="File Operation Error",
                                          message="Can't Update Recipe Image Folder Name !")
                except OSError:
                    Messagebox.show_error(parent=self.amend_ingredient_list_frame, title="File Operation Error",
                                          message="Can't Update Recipe Image Folder Name !")
            else:
                try:
                    image_one_new_path = base_path + image_one_file_name
                    image_two_new_path = base_path + image_two_file_name
                    image_three_new_path = base_path + image_three_file_name
                    print(self.amend_recipe_picture_three_entry.get().strip())
                    print(image_three_new_path)
                    os.replace(src=self.amend_recipe_picture_one_entry.get().strip(), dst=image_one_new_path)
                    os.replace(src=self.amend_recipe_picture_two_entry.get().strip(), dst=image_two_new_path)
                    os.replace(src=self.amend_recipe_picture_three_entry.get().strip(), dst=image_three_new_path)
                    self.amend_update_ingredient_list()
                    Messagebox.show_info(parent=self.amend_ingredient_list_frame, title='Information',
                                         message="Recipe Updated Successfully")
                except IsADirectoryError:
                    Messagebox.show_error(parent=self.amend_ingredient_list_frame, title="File Operation Error",
                                          message="Sorry, But You Are Try To Update Directory, Not A File !")
                except FileNotFoundError:
                    Messagebox.show_error(parent=self.amend_ingredient_list_frame, title="File Operation Error",
                                          message="Can't Find The File Which You Wish To Operate!")
                except OSError:
                    Messagebox.show_error(parent=self.amend_ingredient_list_frame, title="File Operation Error",
                                          message="File Operation Error, Please Check The Images File Path !")


    def amend_update_ingredient_list(self):
        listview_ingredients = self.amend_ingredient_list_table.get_children()
        for each_ingredients in listview_ingredients:
            name = self.amend_ingredient_list_table.item(each_ingredients)['values'][0]
            amount = self.amend_ingredient_list_table.item(each_ingredients)['values'][1].split(" ")[0]
            unit_name = self.amend_ingredient_list_table.item(each_ingredients)['values'][1].split(" ")[1]
            unit_id_search_sql = 'select unit_id from unit where unit_name = ?'
            unit_id = ConnectDatabase(unit_id_search_sql).execute_sql_with_values((unit_name,))[0][0]
            type_id = self.amend_ingredient_list_table.item(each_ingredients)['values'][2]
            self.amend_ingredient_items_list.append([name,amount,unit_id,type_id])

        delete_existing_ingredients_sql = 'delete from recipe_ingredient where recipe_id=?'
        ConnectDatabase(delete_existing_ingredients_sql).execute_sql_with_values((self.current_recipe_id,))

        for each_ingredient in self.amend_ingredient_items_list:
            ingredient_type_match_sql = 'select ingredient_id, ingredient_type from ingredient where ingredient_name=?'
            ingredient_type_match = ConnectDatabase(ingredient_type_match_sql).execute_sql_with_values((each_ingredient[0].lower(),))

            if len(ingredient_type_match)>0:
                if ingredient_type_match[0][1] != str(each_ingredient[3]):
                        update_ingredient_food_type_sql = 'update ingredient set ingredient_type = ? where ingredient_id = ?'
                        ConnectDatabase(update_ingredient_food_type_sql).execute_sql_with_values((each_ingredient[3],ingredient_type_match[0][0]))
            else:
                insert_new_ingredient_sql = "insert into ingredient(ingredient_name, ingredient_type) VALUES (?,?)"
                ConnectDatabase(insert_new_ingredient_sql).execute_insert_query((each_ingredient[0].lower(),each_ingredient[3]))

            get_ingredient_id_sql = 'select ingredient_id from ingredient where ingredient_name = ?'
            get_ingredient_id = ConnectDatabase(get_ingredient_id_sql).execute_sql_with_values((each_ingredient[0].lower(),))[0][0]
            insert_ingredients_to_recipe_sql = 'insert into recipe_ingredient(recipe_id, ingredient_id, amount, unit) values (?,?,?,?)'
            ConnectDatabase(insert_ingredients_to_recipe_sql).execute_insert_query((self.current_recipe_id,get_ingredient_id,each_ingredient[1],each_ingredient[2]))
        self.current_recipe_id = -1
        self.amend_clear_frame()
        self.amend_ingredient_items_list.clear()

    def amend_data_validation(self) -> bool:
        title_check:bool = False
        cooking_time_check:bool = False
        calories_check:bool = False
        image_one_check:bool = False
        image_two_check:bool = False
        image_three_check:bool = False
        ingredient_check:bool = False
        instructions_check:bool = False
        if not InputValidate(self.amend_title_entry.get().strip()).check_text_only():
            Messagebox.show_error(parent=self.amend_ingredient_list_frame, title='Operation Error',
                                  message="Please check the recipe title before update !")
        else:
            title_check = True

        if not InputValidate(self.amend_cooking_time_entry.get().strip()).check_number_only():
            Messagebox.show_error(parent=self.amend_ingredient_list_frame, title='Operation Error',
                                  message="Please check the if you input cooking time correctly !")
        elif int(self.amend_cooking_time_entry.get().strip()) < 5:
            Messagebox.show_error(parent=self.amend_ingredient_list_frame, title='Operation Error',
                                  message="Please check the if you input cooking time correctly !")
        else:
            cooking_time_check = True

        if not InputValidate(self.amend_calories_entry.get().strip()).check_number_only():
            Messagebox.show_error(parent=self.amend_ingredient_list_frame, title='Operation Error',
                                  message="Please check the if you input calories per serve correctly !")
        elif int(self.amend_calories_entry.get().strip()) < 30:
            Messagebox.show_error(parent=self.amend_ingredient_list_frame, title='Operation Error',
                                  message="Please check the if you input calories per serve correctly !")
        else:
            calories_check = True

        if not InputValidate(self.amend_recipe_picture_one_entry.get().strip()).check_picture():
            Messagebox.show_error(parent=self.amend_ingredient_list_frame, title='Operation Error',
                                  message="Loading picture failed, Please check the path for image one !")
        else:
            image_one_check = True

        if not InputValidate(self.amend_recipe_picture_two_entry.get().strip()).check_picture():
            Messagebox.show_error(parent=self.amend_ingredient_list_frame, title='Operation Error',
                                  message="Loading picture failed, Please check the path for image two !")
        else:
            image_two_check = True

        if not InputValidate(self.amend_recipe_picture_three_entry.get().strip()).check_picture():
            Messagebox.show_error(parent=self.amend_ingredient_list_frame, title='Operation Error',
                                  message="Loading picture failed, Please check the path for image three !")
        else:
            image_three_check = True

        if len(self.amend_ingredient_list_table.get_children()) == 0:
            Messagebox.show_error(parent=self.amend_ingredient_list_frame, title='Operation Error',
                                  message="There is no ingredient exist for this recipe. Please double check !")
        else:
            ingredient_check = True

        if len(self.amend_instructions_text.get('1.0',END).strip()) < 50:
            Messagebox.show_error(parent=self.amend_ingredient_list_frame, title='Operation Error',
                                  message="Please make sure the instructions for the recipe are right !")
        else:
            instructions_check = True

        if title_check and cooking_time_check and calories_check and image_one_check and image_two_check and image_three_check and ingredient_check and instructions_check:
            return True

        return False








