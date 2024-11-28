import copy
import tkinter
from tkinter import *
import ttkbootstrap as ttkb
from databaseconnection import ConnectDatabase
from centerscreen import CenterScreen
from recipedetails import RecipeDetails
from ttkbootstrap.dialogs import Messagebox


# noinspection DuplicatedCode
class MainWindow(ttkb.Toplevel):
    COLUMNS = ("Recipe Name", "Dish Type", "Category", "Cooking Time", "Calories Per Serving")

    DIET_CATEGORY: tuple = ('Flexitarian (Normal Diet)',
                            'Pescatarian',
                            'Lacto-ovo-vegetarian',
                            'Lacto-vegetarian',
                            'Ovo-vegetarian',
                            'Vegan',)

    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.recipe_id: str = ""
        self.parent = parent
        self.user_id = user_id
        self.window_width = 1000
        self.window_height = 960
        self.start_point = CenterScreen(screen=self, win_width=self.window_width, win_height=self.window_height)
        self.start_x = self.start_point.start_x
        self.start_y = self.start_point.start_y
        self.geometry(
            f"{self.window_width}x{self.window_height}+{int(self.start_point.start_x)}+"
            f"{int(self.start_point.start_y) - 30}")
        self.title("Recipe Manager")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.order_items_list = []
        self.__main_frame_widgets()
        self.attributes('-topmost', 0)
        #Style('superhero')
        self.mainloop()

    def __main_frame_widgets(self):
        self.favorite_frame = ttkb.LabelFrame(self, text="Your Personal Favorite Recipe List", labelanchor='n',
                                              style='success')
        self.favorite_frame.grid(row=0, column=0, columnspan=2, pady=(35, 10), padx=(30, 0))
        self.favorite_list_table = ttkb.Treeview(self.favorite_frame, columns=self.COLUMNS, show='headings', height=6, )
        self.favorite_list_table.heading("Recipe Name", text="Recipe Name")
        self.favorite_list_table.column("Recipe Name", width=280, anchor=CENTER)
        self.favorite_list_table.heading("Dish Type", text="Dish Type")
        self.favorite_list_table.column("Dish Type", width=150, anchor=CENTER)
        self.favorite_list_table.heading("Category", text="Category")
        self.favorite_list_table.column("Category", width=170, anchor=CENTER)
        self.favorite_list_table.heading("Cooking Time", text="Cooking Time")
        self.favorite_list_table.column("Cooking Time", width=150, anchor=CENTER)
        self.favorite_list_table.heading("Calories Per Serving", text="Calories Per Serving")
        self.favorite_list_table.column("Calories Per Serving", width=130, anchor=CENTER)
        self.favorite_list_table.pack(pady=(25,15), padx=25)
        self.remove_from_favorite_button = ttkb.Button(self.favorite_frame, text='Remove Recipe From My Favorite',
                                                       width=143,style="danger,outline",command= self.remove_from_favorite)
        self.remove_from_favorite_button.pack(pady=(5,20))
        self.remove_from_favorite_button.config(state=DISABLED)
        self.favorite_list_table.bind('<Double-Button-1>', self.favorite_table_double_click)
        self.favorite_list_table.bind('<<TreeviewSelect>>',self.favorite_table_row_select)


        self.search_label_frame = ttkb.LabelFrame(self, text="Search Recipes", style='info')
        self.search_label_frame.grid(row=1, column=0, pady=(15, 10), padx=(30, 0))
        self.search_entry = ttkb.Entry(self.search_label_frame, width=100, style='info', justify='center')
        self.search_entry.insert(tkinter.END, 'Use Keyword to Search Recipes')
        self.search_entry.bind("<Enter>", self.search_widget_enter)
        self.search_entry.grid(row=0, column=0, padx=(25, 5), pady=(15, 0), sticky=W)
        self.search_button = ttkb.Button(self.search_label_frame, text="Search Recipes",width=30 ,style='warning',
                                         command=self.keywords_search_recipes_loaded)
        self.search_button.grid(row=0, column=1, padx=(5, 20), ipadx=25, pady=(15, 0))
        self.search_result_table = ttkb.Treeview(self.search_label_frame, columns=self.COLUMNS, show='headings',
                                                 height=6, )
        self.search_result_table.heading("Recipe Name", text="Recipe Name")
        self.search_result_table.column("Recipe Name", width=280, anchor=CENTER)
        self.search_result_table.heading("Dish Type", text="Dish Type")
        self.search_result_table.column("Dish Type", width=150, anchor=CENTER)
        self.search_result_table.heading("Category", text="Category")
        self.search_result_table.column("Category", width=170, anchor=CENTER)
        self.search_result_table.heading("Cooking Time", text="Cooking Time")
        self.search_result_table.column("Cooking Time", width=150, anchor=CENTER)
        self.search_result_table.heading("Calories Per Serving", text="Calories Per Serving")
        self.search_result_table.column("Calories Per Serving", width=130, anchor=CENTER)
        self.search_result_table.grid(row=1, column=0, pady=(15, 25), padx=25, columnspan=2)
        self.search_add_to_favorite_button = ttkb.Button(self.search_label_frame, text="Add Recipe To My Favorite",
                                                         style="info,outline", width=143,
                                                         command= lambda: self.add_recipe_to_favorite('Search Result'))
        self.search_add_to_favorite_button.grid(row=2, column=0, padx=25, pady=(0, 20), columnspan=2)
        self.search_add_to_favorite_button.config(state=DISABLED)
        self.search_result_table.bind('<Double-Button-1>', self.search_table_double_click)
        self.search_result_table.bind('<<TreeviewSelect>>', self.search_table_row_select)


        self.categorized_recipes_frame = ttkb.LabelFrame(self, text="Explore Categorized Recipes", style='warning',
                                                         labelanchor='ne')
        self.categorized_recipes_frame.grid(row=2, column=0, pady=(15, 10), padx=(30, 0))
        self.recipe_notebook = ttkb.Notebook(self.categorized_recipes_frame, )

        self.meaty_one_frame = ttkb.Frame(self.recipe_notebook)
        self.meaty_one_table = ttkb.Treeview(self.meaty_one_frame, columns=self.COLUMNS, show='headings', height=8, )
        self.meaty_one_table.heading("Recipe Name", text="Recipe Name")
        self.meaty_one_table.column("Recipe Name", width=270, anchor=CENTER)
        self.meaty_one_table.heading("Dish Type", text="Dish Type")
        self.meaty_one_table.column("Dish Type", width=130, anchor=CENTER)
        self.meaty_one_table.heading("Category", text="Category")
        self.meaty_one_table.column("Category", width=170, anchor=CENTER)
        self.meaty_one_table.heading("Cooking Time", text="Cooking Time")
        self.meaty_one_table.column("Cooking Time", width=130, anchor=CENTER)
        self.meaty_one_table.heading("Calories Per Serving", text="Calories Per Serving")
        self.meaty_one_table.column("Calories Per Serving", width=130, anchor=CENTER)
        self.meaty_one_table.grid(row=0, column=0, pady=(15, 25), padx=25)
        self.meaty_add_to_favorite_button = ttkb.Button(self.meaty_one_frame, text="Add to My Favorite", style="info,outline",
                                                        width=135, command= lambda: self.add_recipe_to_favorite('Meaty One'))
        self.meaty_add_to_favorite_button.grid(row=1, column=0, padx=25, pady=(0, 15))
        self.meaty_add_to_favorite_button.config(state=DISABLED)
        self.meaty_one_table.bind('<Double-Button-1>', self.meaty_one_double_click)
        self.meaty_one_table.bind('<<TreeviewSelect>>', self.meaty_one_row_select)



        self.fish_seafood_frame = ttkb.Frame(self.recipe_notebook)
        self.fish_seafood_table = ttkb.Treeview(self.fish_seafood_frame, columns=self.COLUMNS, show='headings',
                                                height=8, )
        self.fish_seafood_table.heading("Recipe Name", text="Recipe Name")
        self.fish_seafood_table.column("Recipe Name", width=270, anchor=CENTER)
        self.fish_seafood_table.heading("Dish Type", text="Dish Type")
        self.fish_seafood_table.column("Dish Type", width=130, anchor=CENTER)
        self.fish_seafood_table.heading("Category", text="Category")
        self.fish_seafood_table.column("Category", width=170, anchor=CENTER)
        self.fish_seafood_table.heading("Cooking Time", text="Cooking Time")
        self.fish_seafood_table.column("Cooking Time", width=130, anchor=CENTER)
        self.fish_seafood_table.heading("Calories Per Serving", text="Calories Per Serving")
        self.fish_seafood_table.column("Calories Per Serving", width=130, anchor=CENTER)
        self.fish_seafood_table.grid(row=0, column=0, pady=(15, 25), padx=25)
        self.fish_add_to_favorite_button = ttkb.Button(self.fish_seafood_frame, text="Add to My Favorite",
                                                       style="info,outline", width=135,
                                                       command= lambda: self.add_recipe_to_favorite('Seafood And Shellfish'))
        self.fish_add_to_favorite_button.grid(row=1, column=0, padx=25, pady=(0, 15))
        self.fish_add_to_favorite_button.config(state=DISABLED)
        self.fish_seafood_table.bind('<Double-Button-1>', self.seafood_double_click)
        self.fish_seafood_table.bind('<<TreeviewSelect>>', self.fish_seafood_row_select)

        self.rice_noddle_pasta_frame = ttkb.Frame(self.recipe_notebook)
        self.rice_noddle_pasta_table = ttkb.Treeview(self.rice_noddle_pasta_frame, columns=self.COLUMNS,
                                                     show='headings',
                                                     height=8, )
        self.rice_noddle_pasta_table.heading("Recipe Name", text="Recipe Name")
        self.rice_noddle_pasta_table.column("Recipe Name", width=270, anchor=CENTER)
        self.rice_noddle_pasta_table.heading("Dish Type", text="Dish Type")
        self.rice_noddle_pasta_table.column("Dish Type", width=130, anchor=CENTER)
        self.rice_noddle_pasta_table.heading("Category", text="Category")
        self.rice_noddle_pasta_table.column("Category", width=170, anchor=CENTER)
        self.rice_noddle_pasta_table.heading("Cooking Time", text="Cooking Time")
        self.rice_noddle_pasta_table.column("Cooking Time", width=130, anchor=CENTER)
        self.rice_noddle_pasta_table.heading("Calories Per Serving", text="Calories Per Serving")
        self.rice_noddle_pasta_table.column("Calories Per Serving", width=130, anchor=CENTER)
        self.rice_noddle_pasta_table.grid(row=0, column=0, pady=(15, 25), padx=25)
        self.rice_add_to_favorite_button = ttkb.Button(self.rice_noddle_pasta_frame, text="Add to My Favorite",
                                                       style="info,outline", width=135,
                                                       command= lambda: self.add_recipe_to_favorite('Rice And Noodles Dish'))
        self.rice_add_to_favorite_button.grid(row=1, column=0, padx=25, pady=(0, 15))
        self.rice_add_to_favorite_button.config(state=DISABLED)
        self.rice_noddle_pasta_table.bind('<Double-Button-1>', self.rice_noddles_table_double_click)
        self.rice_noddle_pasta_table.bind('<<TreeviewSelect>>', self.rice_noddle_pasta_row_select)

        self.dessert_frame = ttkb.Frame(self.recipe_notebook)
        self.dessert_table = ttkb.Treeview(self.dessert_frame, columns=self.COLUMNS, show='headings', height=8, )
        self.dessert_table.heading("Recipe Name", text="Recipe Name")
        self.dessert_table.column("Recipe Name", width=270, anchor=CENTER)
        self.dessert_table.heading("Dish Type", text="Dish Type")
        self.dessert_table.column("Dish Type", width=130, anchor=CENTER)
        self.dessert_table.heading("Category", text="Category")
        self.dessert_table.column("Category", width=170, anchor=CENTER)
        self.dessert_table.heading("Cooking Time", text="Cooking Time")
        self.dessert_table.column("Cooking Time", width=130, anchor=CENTER)
        self.dessert_table.heading("Calories Per Serving", text="Calories Per Serving")
        self.dessert_table.column("Calories Per Serving", width=130, anchor=CENTER)
        self.dessert_table.grid(row=0, column=0, pady=(15, 25), padx=25)
        self.dessert_add_to_favorite_button = ttkb.Button(self.dessert_frame, text="Add to My Favorite",
                                                          style="info,outline", width=135,
                                                          command= lambda: self.add_recipe_to_favorite('Desserts'))
        self.dessert_add_to_favorite_button.grid(row=1, column=0, padx=25, pady=(0, 15))
        self.dessert_add_to_favorite_button.config(state=DISABLED)
        self.dessert_table.bind('<Double-Button-1>', self.desserts_table_double_click)
        self.dessert_table.bind('<<TreeviewSelect>>', self.dessert_row_select)

        self.vegan_vegetarian_frame = ttkb.Frame(self.recipe_notebook)
        self.vegan_vegetarian_table = ttkb.Treeview(self.vegan_vegetarian_frame, columns=self.COLUMNS, show='headings',
                                                    height=8, )
        self.vegan_vegetarian_table.heading("Recipe Name", text="Recipe Name")
        self.vegan_vegetarian_table.column("Recipe Name", width=270, anchor=CENTER)
        self.vegan_vegetarian_table.heading("Dish Type", text="Dish Type")
        self.vegan_vegetarian_table.column("Dish Type", width=130, anchor=CENTER)
        self.vegan_vegetarian_table.heading("Category", text="Category")
        self.vegan_vegetarian_table.column("Category", width=170, anchor=CENTER)
        self.vegan_vegetarian_table.heading("Cooking Time", text="Cooking Time")
        self.vegan_vegetarian_table.column("Cooking Time", width=130, anchor=CENTER)
        self.vegan_vegetarian_table.heading("Calories Per Serving", text="Calories Per Serving")
        self.vegan_vegetarian_table.column("Calories Per Serving", width=130, anchor=CENTER)
        self.vegan_vegetarian_table.grid(row=0, column=0, pady=(15, 25), padx=25)
        self.vegan_add_to_favorite_button = ttkb.Button(self.vegan_vegetarian_frame, text="Add to My Favorite",
                                                        style="info,outline", width=135,
                                                        command= lambda: self.add_recipe_to_favorite('Vegan'))
        self.vegan_add_to_favorite_button.grid(row=1, column=0, padx=25, pady=(0, 15))
        self.vegan_add_to_favorite_button.config(state=DISABLED)
        self.vegan_vegetarian_table.bind('<Double-Button-1>', self.vegan_table_double_click)
        self.vegan_vegetarian_table.bind('<<TreeviewSelect>>', self.vegan_vegetarian_row_select)

        self.cooking_time_frame = ttkb.Frame(self.recipe_notebook)
        self.cooking_time_table = ttkb.Treeview(self.cooking_time_frame, columns=self.COLUMNS, show='headings',
                                                height=8)
        self.cooking_time_table.heading("Recipe Name", text="Recipe Name")
        self.cooking_time_table.column("Recipe Name", width=270, anchor=CENTER)
        self.cooking_time_table.heading("Dish Type", text="Dish Type")
        self.cooking_time_table.column("Dish Type", width=130, anchor=CENTER)
        self.cooking_time_table.heading("Category", text="Category")
        self.cooking_time_table.column("Category", width=170, anchor=CENTER)
        self.cooking_time_table.heading("Cooking Time", text="Cooking Time")
        self.cooking_time_table.column("Cooking Time", width=130, anchor=CENTER)
        self.cooking_time_table.heading("Calories Per Serving", text="Calories Per Serving")
        self.cooking_time_table.column("Calories Per Serving", width=130, anchor=CENTER)
        self.cooking_time_table.grid(row=0, column=0, pady=(15, 25), padx=25)
        self.cooking_time_add_to_favorite_button = ttkb.Button(self.cooking_time_frame, text="Add to My Favorite",
                                                               style="info,outline", width=135,
                                                               command= lambda: self.add_recipe_to_favorite('Cooking Under 30mins'))
        self.cooking_time_add_to_favorite_button.grid(row=1, column=0, padx=25, pady=(0, 15))
        self.cooking_time_add_to_favorite_button.config(state=DISABLED)
        self.cooking_time_table.bind('<Double-Button-1>', self.cooking_under_30mins_table_click)
        self.cooking_time_table.bind('<<TreeviewSelect>>', self.cooking_under_60mins_table_row_select)

        self.recipe_notebook.add(self.meaty_one_frame, text='Meaty One')
        self.recipe_notebook.add(self.fish_seafood_frame, text='Fish and Seafood')
        self.recipe_notebook.add(self.rice_noddle_pasta_frame, text='Rice, Noddle and Pasta')
        self.recipe_notebook.add(self.dessert_frame, text='Dessert As Always')
        self.recipe_notebook.add(self.vegan_vegetarian_frame, text='Vegan and Vegetarian')
        self.recipe_notebook.add(self.cooking_time_frame, text='Meal Ready in 30 Minutes')
        self.recipe_notebook.pack(pady=25, padx=25)
        self.load_recipes()
        self.load_favorites()

    def search_widget_enter(self, event):
        self.search_entry.delete('0', END)

    def meaty_one_row_select(self, event):
        if len(self.meaty_one_table.get_children()) > 0:
            if len(self.meaty_one_table.selection()) > 0 :
                self.meaty_add_to_favorite_button.config(state=NORMAL)
                self.recipe_id = self.meaty_one_table.selection()[0]
        else:
            self.meaty_add_to_favorite_button.config(state=DISABLED)

    def favorite_table_row_select(self,event):
        if len(self.favorite_list_table.get_children()) > 0:
            if len(self.favorite_list_table.selection()) > 0 :
                self.remove_from_favorite_button.config(state=NORMAL)
                self.recipe_id = self.favorite_list_table.selection()[0]
        else:
            self.remove_from_favorite_button.config(state=DISABLED)

    def fish_seafood_row_select(self,event):
        if len(self.fish_seafood_table.get_children()) > 0:
            if len(self.fish_seafood_table.selection()) > 0:
                self.fish_add_to_favorite_button.config(state=NORMAL)
                self.recipe_id = self.fish_seafood_table.selection()[0]
        else:
            self.fish_add_to_favorite_button.config(state=DISABLED)

    def rice_noddle_pasta_row_select(self,event):
        if len(self.rice_noddle_pasta_table.get_children()) > 0:
            if len(self.rice_noddle_pasta_table.selection()) > 0:
                self.rice_add_to_favorite_button.config(state=NORMAL)
                self.recipe_id = self.rice_noddle_pasta_table.selection()[0]
        else:
            self.rice_add_to_favorite_button.config(state=DISABLED)

    def dessert_row_select(self,event):
        if len(self.dessert_table.get_children()) > 0:
            if len(self.dessert_table.selection()) > 0:
                self.dessert_add_to_favorite_button.config(state=NORMAL)
                self.recipe_id = self.dessert_table.selection()[0]
        else:
            self.dessert_add_to_favorite_button.config(state=DISABLED)

    def vegan_vegetarian_row_select(self,event):
        if len(self.vegan_vegetarian_table.get_children()) > 0:
            if len(self.vegan_vegetarian_table.selection()) > 0:
                self.vegan_add_to_favorite_button.config(state=NORMAL)
                self.recipe_id = self.vegan_vegetarian_table.selection()[0]
        else:
            self.vegan_add_to_favorite_button.config(state=DISABLED)

    def cooking_under_60mins_table_row_select(self,event):
        if len(self.cooking_time_table.get_children()) > 0:
            if len(self.cooking_time_table.selection()) > 0:
                self.cooking_time_add_to_favorite_button.config(state=NORMAL)
                self.recipe_id = self.cooking_time_table.selection()[0]
        else:
            self.cooking_time_add_to_favorite_button.config(state=DISABLED)

    def search_table_row_select(self,event):
        if len(self.search_result_table.get_children()) > 0:
            if len(self.search_result_table.selection()) > 0:
                self.search_add_to_favorite_button.config(state=NORMAL)
                self.recipe_id = self.search_result_table.selection()[0]
        else:
            self.search_add_to_favorite_button.config(state=DISABLED)

    def add_recipe_to_favorite(self,table_name:str):
        single_recipes_sql: str = (
            f"SELECT recipes.recipe_id, recipes.recipe_name,recipes.cooking_time,recipes.calories_per_serving,recipes.recipe_category,"
            f"c.category_name,d.dish_type FROM recipes INNER JOIN main.category c "
            f"on c.category_id = recipes.category_id INNER JOIN main.dish d "
            f"on d.dish_id = recipes.dish_id where recipes.recipe_id = ?")
        recipe_result: list = ConnectDatabase(single_recipes_sql).execute_sql_with_values((self.recipe_id,))
        self.favorite_list_table.insert('', 'end', iid=self.recipe_id, values=[
            recipe_result[0][1].title(),
            recipe_result[0][6].title(),
            recipe_result[0][5].title(),
            recipe_result[0][2].title(),
            recipe_result[0][3]])
        if table_name == 'Meaty One':
            if int(recipe_result[0][2].split(' ')[0]) > 30:
                self.meaty_one_table.delete(self.meaty_one_table.selection()[0])
                self.meaty_add_to_favorite_button.config(state=DISABLED)
                self.favorite_in_search_table_check(self.recipe_id)
            else:
                recipe_id = self.meaty_one_table.selection()[0]
                self.meaty_one_table.delete(recipe_id)
                self.meaty_add_to_favorite_button.config(state=DISABLED)
                self.cooking_time_table.delete(recipe_id)
                self.favorite_in_search_table_check(self.recipe_id)
        elif table_name =='Seafood And Shellfish':
            if int(recipe_result[0][2].split(' ')[0]) > 30:
                self.fish_seafood_table.delete(self.fish_seafood_table.selection()[0])
                self.fish_add_to_favorite_button.config(state=DISABLED)
                self.favorite_in_search_table_check(self.recipe_id)
            else:
                recipe_id = self.fish_seafood_table.selection()[0]
                self.fish_seafood_table.delete(recipe_id)
                self.fish_add_to_favorite_button.config(state=DISABLED)
                self.cooking_time_table.delete(recipe_id)
                self.favorite_in_search_table_check(self.recipe_id)
        elif table_name == 'Rice And Noodles Dish':
            if int(recipe_result[0][2].split(' ')[0]) > 30:
                self.rice_noddle_pasta_table.delete(self.rice_noddle_pasta_table.selection()[0])
                self.rice_add_to_favorite_button.config(state=DISABLED)
                self.favorite_in_search_table_check(self.recipe_id)
            else:
                recipe_id = self.rice_noddle_pasta_table.selection()[0]
                self.rice_noddle_pasta_table.delete(recipe_id)
                self.rice_add_to_favorite_button.config(state=DISABLED)
                self.cooking_time_table.delete(recipe_id)
                self.favorite_in_search_table_check(self.recipe_id)
        elif table_name == 'Desserts':
            if int(recipe_result[0][2].split(' ')[0]) > 30:
                self.dessert_table.delete(self.dessert_table.selection()[0])
                self.dessert_add_to_favorite_button.config(state=DISABLED)
                self.favorite_in_search_table_check(self.recipe_id)
            else:
                recipe_id = self.dessert_table.selection()[0]
                self.dessert_table.delete(recipe_id)
                self.dessert_add_to_favorite_button.config(state=DISABLED)
                self.cooking_time_table.delete(recipe_id)
                self.favorite_in_search_table_check(self.recipe_id)
        elif table_name == 'Vegan':
            if int(recipe_result[0][2].split(' ')[0]) > 30:
                self.vegan_vegetarian_table.delete(self.vegan_vegetarian_table.selection()[0])
                self.vegan_add_to_favorite_button.config(state=DISABLED)
                self.favorite_in_search_table_check(self.recipe_id)
            else:
                recipe_id = self.vegan_vegetarian_table.selection()[0]
                self.vegan_vegetarian_table.delete(recipe_id)
                self.vegan_add_to_favorite_button.config(state=DISABLED)
                self.cooking_time_table.delete(recipe_id)
                self.favorite_in_search_table_check(self.recipe_id)
        elif table_name == 'Cooking Under 30mins' or table_name == 'Search Result':
            if table_name == 'Cooking Under 30mins':
                recipe_id = self.cooking_time_table.selection()[0]
                self.cooking_time_table.delete(self.cooking_time_table.selection()[0])
                self.cooking_time_add_to_favorite_button.config(state=DISABLED)
                self.favorite_in_search_table_check(self.recipe_id)
            else:
                recipe_id = self.search_result_table.selection()[0]
                self.search_result_table.delete(self.search_result_table.selection()[0])
                self.search_add_to_favorite_button.config(state=DISABLED)
                if recipe_id in self.cooking_time_table.get_children():
                    self.cooking_time_table.delete(recipe_id)
            match recipe_result[0][4].title():
                case 'Meaty One':
                    self.meaty_one_table.delete(recipe_id)
                case 'Seafood And Shellfish':
                    self.fish_seafood_table.delete(recipe_id)
                case 'Rice And Noodles Dish':
                    self.rice_noddle_pasta_table.delete(recipe_id)
                case 'Vegan':
                    self.vegan_vegetarian_table.delete(recipe_id)
                case 'Desserts':
                    self.dessert_table.delete(recipe_id)

        add_favorite_to_database = 'INSERT INTO user_favorite_list(user_id, recipe_id) VALUES(?,?)'
        ConnectDatabase(add_favorite_to_database).execute_insert_query((self.user_id,self.recipe_id),)



    def load_favorites(self):
        load_favorites_recipes_sql: str = (f"SELECT recipes.recipe_id, recipes.recipe_name,recipes.cooking_time,recipes.calories_per_serving,recipes.recipe_category,"
                              f"c.category_name,d.dish_type FROM recipes INNER JOIN main.category c "
                              f"on c.category_id = recipes.category_id INNER JOIN main.dish d "
                              f"on d.dish_id = recipes.dish_id INNER JOIN user_favorite_list u on recipes.recipe_id = u.recipe_id and u.user_id = ?")
        favorites_recipes_result: list = ConnectDatabase(load_favorites_recipes_sql).execute_sql_with_values((self.user_id,))
        for each_recipe in favorites_recipes_result:
            self.insert_item(each_recipe,self.favorite_list_table)


    def load_recipes(self):
        recipe_data: list = self.get_recipes_loaded()
        for each_recipe in recipe_data:
            match each_recipe[4].title():
                case 'Meaty One': self.insert_item(each_recipe,self.meaty_one_table)
                case 'Seafood And Shellfish': self.insert_item(each_recipe,self.fish_seafood_table)
                case 'Rice And Noodles Dish': self.insert_item(each_recipe, self.rice_noddle_pasta_table)
                case 'Vegan': self.insert_item(each_recipe, self.vegan_vegetarian_table)
                case 'Desserts': self.insert_item(each_recipe, self.dessert_table)
            if int(each_recipe[2].split(" ")[0]) <= 30:
                self.insert_item(each_recipe, self.cooking_time_table)

    def insert_item(self, each_recipe, frame_table) -> None:
        frame_table.insert('', 'end', iid=each_recipe[0],
                           values=[each_recipe[1].title(), each_recipe[6], each_recipe[5],
                                   each_recipe[2], each_recipe[3]])



    def get_recipes_loaded(self) -> list:
        user_favorite_exist_sql: str = "SELECT recipe_id FROM user_favorite_list WHERE user_id = ?"
        user_favorite_recipes_result: list = ConnectDatabase(user_favorite_exist_sql).execute_sql_with_values((self.user_id,))
        remove_index_list: list = []
        vegan_recipe:list = []
        user_allergy_list: list = []
        if len(user_favorite_recipes_result) != 0:
            load_all_recipes_sql: str = (f"SELECT recipes.recipe_id, recipes.recipe_name,recipes.cooking_time,recipes.calories_per_serving,recipes.recipe_category, "
                                  f"c.category_name,d.dish_type FROM recipes INNER JOIN main.category c "
                                  f"on c.category_id = recipes.category_id INNER JOIN main.dish d "
                                  f"on d.dish_id = recipes.dish_id")
            recipes_result: list = ConnectDatabase(load_all_recipes_sql).execute_sql_without_values()
            for recipe_index in range(len(recipes_result)):
                for each_favorite in user_favorite_recipes_result:
                    if each_favorite[0] == recipes_result[recipe_index][0]:
                        remove_index_list.append(recipe_index)
            for each_index in reversed(remove_index_list):
                recipes_result.pop(each_index)
        else:
            load_all_recipes_sql: str = (
                f"SELECT recipes.recipe_id, recipes.recipe_name,recipes.cooking_time,recipes.calories_per_serving,recipes.recipe_category,"
                f"c.category_name,d.dish_type FROM recipes INNER JOIN main.category c "
                f"on c.category_id = recipes.category_id INNER JOIN main.dish d "
                f"on d.dish_id = recipes.dish_id")
            recipes_result: list = ConnectDatabase(load_all_recipes_sql).execute_sql_without_values()

        # Check user's diet preference,exclude those recipe which not fulfill user's requirement
        user_diet_preference_sql: str = "select diet_preference,halal_food from users where user_id = ?"
        user_diet_preference = ConnectDatabase(user_diet_preference_sql).execute_sql_with_values((self.user_id,))

        user_allergy_list_sql: str =("select f.type_name from user_allergy_list inner join food_type_list f on "
                                     "user_allergy_list.allergy_type = f.type_id where user_id = ?")
        user_allergy_list_result = ConnectDatabase(user_allergy_list_sql).execute_sql_with_values((self.user_id,))
        for each_allergy_type in user_allergy_list_result:
            user_allergy_list.append(each_allergy_type[0])

        if len(user_diet_preference) != 0:
            if user_diet_preference[0][1] == "Yes":
                halal_remove_index_list: list = []
                recipes_result_copy = copy.deepcopy(recipes_result)
                for index,each_recipe in enumerate(recipes_result_copy):
                    search_recipe_ingredient_sql:str = ("select i.ingredient_name, f.type_name from recipes "
                                                        "INNER JOIN recipe_ingredient r on recipes.recipe_id = r.recipe_id "
                                                        "inner join ingredient i on r.ingredient_id = i.ingredient_id "
                                                        "INNER JOIN food_type_list f on i.ingredient_type = f.type_id "
                                                        "where recipes.recipe_id = ?")
                    search_recipe_ingredient_result: list = ConnectDatabase(search_recipe_ingredient_sql).execute_sql_with_values((each_recipe[0],))
                    for each_ingredient in search_recipe_ingredient_result:
                        if "pork" in each_ingredient[0] or "chorizo" in each_ingredient[0] or "bacon" in each_ingredient[0]:
                            halal_remove_index_list.append(index)
                            break
                for each_index in reversed(halal_remove_index_list):
                    recipes_result.pop(each_index)

            if user_diet_preference[0][0] != "Flexitarian (Normal Diet)":
                for each_recipe in recipes_result:
                    if each_recipe[4].title() == "Vegan":
                        vegan_recipe.append(each_recipe)
                recipes_result.clear()
                recipes_result = vegan_recipe

        # Check user's allergy list, exclude recipes which contain user's allergy ingredient.
            if len(user_allergy_list) > 0 :
                allergy_remove_index_list: list = []
                recipes_result_copy = copy.deepcopy(recipes_result)
                for index, each_recipe in enumerate(recipes_result_copy):
                    search_recipe_ingredient_sql: str = ("select i.ingredient_name, f.type_name from recipes "
                                                         "INNER JOIN recipe_ingredient r on recipes.recipe_id = r.recipe_id "
                                                         "inner join ingredient i on r.ingredient_id = i.ingredient_id "
                                                         "INNER JOIN food_type_list f on i.ingredient_type = f.type_id "
                                                         "where recipes.recipe_id = ?")
                    search_recipe_ingredient_result: list = ConnectDatabase(
                        search_recipe_ingredient_sql).execute_sql_with_values((each_recipe[0],))
                    for each_ingredient in search_recipe_ingredient_result:
                        if each_ingredient[1] in user_allergy_list:
                            allergy_remove_index_list.append(index)
                            break
                for each_index in reversed(allergy_remove_index_list):
                    recipes_result.pop(each_index)
        return recipes_result


    def keywords_search_recipes_loaded(self):
        for each_row in self.search_result_table.get_children():
            self.search_result_table.delete(each_row)
        load_all_recipes_sql: str = (
            f"SELECT recipes.recipe_id, recipes.recipe_name,recipes.cooking_time,recipes.calories_per_serving,recipes.recipe_category,"
            f"c.category_name,d.dish_type FROM recipes INNER JOIN main.category c "
            f"on c.category_id = recipes.category_id INNER JOIN main.dish d "
            f"on d.dish_id = recipes.dish_id where recipes.recipe_name LIKE ? ")
        keyword_search_result: list = ConnectDatabase(load_all_recipes_sql).execute_sql_with_values(('%'+self.search_entry.get().strip()+'%',))
        for each_recipe in keyword_search_result:
            if str(each_recipe[0]) not in self.favorite_list_table.get_children():
                self.insert_item(each_recipe, self.search_result_table)

    def close_window(self):
        user_quit_confirmation:str = Messagebox.yesno(parent=self.search_label_frame,message="Are you sure you want to log out the app?",title="User Confirmation")
        if user_quit_confirmation == "Yes":
            self.destroy()
            self.parent.deiconify()
            self.parent.username_entry.focus()


    def meaty_one_double_click(self,event):
        if len(self.meaty_one_table.get_children()) > 0 :
            recipe_id: str = self.meaty_one_table.selection()[0]
            RecipeDetails(self.parent, recipe_id)

    def seafood_double_click(self,event):
        if len(self.fish_seafood_table.get_children()) > 0:
            recipe_id: str = self.fish_seafood_table.selection()[0]
            RecipeDetails(self.parent, recipe_id)

    def favorite_table_double_click(self,event):
        if len(self.favorite_list_table.get_children()) > 0:
            recipe_id: str = self.favorite_list_table.selection()[0]
            RecipeDetails(self.parent, recipe_id)

    def rice_noddles_table_double_click(self,event):
        if len(self.rice_noddle_pasta_table.get_children()) > 0:
            recipe_id: str = self.rice_noddle_pasta_table.selection()[0]
            RecipeDetails(self.parent, recipe_id)

    def search_table_double_click(self,event):
        if len(self.search_result_table.get_children()) > 0:
            recipe_id: str = self.search_result_table.selection()[0]
            RecipeDetails(self.parent, recipe_id)

    def vegan_table_double_click(self,event):
        if len(self.vegan_vegetarian_table.get_children()) > 0:
            recipe_id: str = self.vegan_vegetarian_table.selection()[0]
            RecipeDetails(self.parent, recipe_id)

    def desserts_table_double_click(self,event):
        if len(self.dessert_table.get_children()) > 0:
            recipe_id: str = self.dessert_table.selection()[0]
            RecipeDetails(self.parent, recipe_id)

    def cooking_under_30mins_table_click(self, event):
        if len(self.cooking_time_table.get_children()) > 0:
            recipe_id: str = self.cooking_time_table.selection()[0]
            RecipeDetails(self.parent, recipe_id)


    def remove_from_favorite(self):
        if len(self.favorite_list_table.selection()) >0 :
            current_recipe_id: str = self.favorite_list_table.selection()[0]
            delete_favorite_recipe_sql:str = "Delete from user_favorite_list where recipe_id = ? and user_id = ?"
            ConnectDatabase(delete_favorite_recipe_sql).execute_delete_query((current_recipe_id,self.user_id))
            self.favorite_list_table.delete(current_recipe_id)
            recipe_details_sql: str = (
                    f"SELECT recipes.recipe_id, recipes.recipe_name,recipes.cooking_time,recipes.calories_per_serving,recipes.recipe_category,"
                    f"c.category_name,d.dish_type FROM recipes INNER JOIN main.category c "
                    f"on c.category_id = recipes.category_id INNER JOIN main.dish d "
                    f"on d.dish_id = recipes.dish_id where recipes.recipe_id = ?")
            recipe_details = ConnectDatabase(recipe_details_sql).execute_sql_with_values((current_recipe_id,))[0]
            match recipe_details[4].title():
                case "Meaty One": self.insert_item(recipe_details, self.meaty_one_table)
                case "Seafood And Shellfish" : self.insert_item(recipe_details, self.fish_seafood_table)
                case "Rice And Noodles Dish" : self.insert_item(recipe_details, self.rice_noddle_pasta_table)
                case "Desserts": self.insert_item(recipe_details, self.dessert_table)
                case "Vegan": self.insert_item(recipe_details, self.vegan_vegetarian_table)
            if int(recipe_details[2].split(" ")[0]) <= 30:
                self.insert_item(recipe_details, self.cooking_time_table)
            self.remove_from_favorite_button.config(state=DISABLED)
        else:
            Messagebox.show_error(parent=self.favorite_frame,title="Error Message",message="Please select the recipe you want to remove")

    def favorite_in_search_table_check(self,recipe_id):
        if len(self.search_result_table.get_children()) and recipe_id in self.search_result_table.get_children():
            self.search_result_table.delete(recipe_id)

