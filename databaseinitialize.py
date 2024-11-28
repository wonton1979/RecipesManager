import sqlite3
import os
import json

SERVING_TYPE: tuple = (('Breakfast',), ('Lunch',), ('Dinner',), ('Desserts',))
DIET_CATEGORY: tuple = (
        ('Flexitarian (Normal Diet)',), ('Pescatarian',), ('Lacto-ovo-vegetarian',), ('Lacto-vegetarian',),
        ('Ovo-vegetarian',), ('Vegan',))
UNIT: tuple = (('Gram',), ('Ml',), ('Tablespoon',), ('Unit',), ('Pinch',),('Slice',))
FOOD_TYPE: tuple = (('Meat',), ('Poultry',), ('Fish',), ('Seafood And Shellfish',), ('Vegetables',),
                    ('Dairy Product',), ('Cooking Oil',), ('Tree Nuts',), ('Egg',), ('Fruit',), ('Grain Product',),
                    ('Seasoning',), ('Soy',), ('Sesame',), ('Peanuts',), ('Yeast',), ('Water',), ('Cocoa Product',),
                    ('Dry Fruit',),('Dry Chemical Leavening Agent',),('Wine',),('Liquor',),('Cider',))

CREATE_TABLE_STATEMENTS: list = [
        """CREATE TABLE IF NOT EXISTS users (
                   user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT NOT NULL UNIQUE, 
                   password TEXT NOT NULL, 
                   email TEXT NOT NULL UNIQUE, 
                   diet_preference TEXT NOT NULL,
                   halal_food TEXT NOT NULL,
                   admin_account INTEGER DEFAULT 0,
                   FOREIGN KEY (user_id) 
                       REFERENCES user_allergy_list (user_id) 
                           ON DELETE CASCADE 
                           ON UPDATE NO ACTION,
                   FOREIGN KEY (user_id)
                       REFERENCES user_favoriate_list (user_id) 
                           ON DELETE CASCADE 
                           ON UPDATE NO ACTION
                       );""",

        """CREATE TABLE IF NOT EXISTS user_allergy_list (
                                           user_id INTEGER,
                                           allergy_type INTEGER NOT NULL,
                                           PRIMARY KEY (user_id, allergy_type),
                                           FOREIGN KEY (allergy_type) 
                                               REFERENCES food_tpye_list (type_id) 
                                                   ON DELETE CASCADE 
                                                   ON UPDATE NO ACTION
                                               );""",

        """CREATE TABLE IF NOT EXISTS user_favorite_list (
                                    user_id INTEGER NOT NULL,
                                    recipe_id INTEGER NOT NULL,
                                    PRIMARY KEY (user_id, recipe_id),
                                    FOREIGN KEY (recipe_id) 
                                        REFERENCES recipes (recipe_id) 
                                            ON DELETE CASCADE 
                                            ON UPDATE NO ACTION,
                                    FOREIGN KEY (user_id) 
                                        REFERENCES users (user_id) 
                                            ON DELETE CASCADE 
                                            ON UPDATE NO ACTION
                                        );""",

        """CREATE TABLE IF NOT EXISTS food_type_list (
                            type_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            type_name TEXT NOT NULL
                                );""",

        """CREATE TABLE IF NOT EXISTS recipes (
            recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_name TEXT NOT NULL UNIQUE,
            category_id INTEGER NOT NULL,
            instructions TEXT NOT NULL UNIQUE,
            image_one TEXT NOT NULL UNIQUE,
            image_two TEXT NOT NULL UNIQUE,
            image_three TEXT NOT NULL UNIQUE,
            cooking_time TEXT NOT NULL,
            recipe_category TEXT NOT NULL, 
            dish_id INTEGER NOT NULL,
            calories_per_serving INTEGER NOT NULL,
            is_halal_food INTEGER NOT NULL,
            FOREIGN KEY (category_id) 
                REFERENCES category (category_id) 
                    ON DELETE CASCADE 
                    ON UPDATE NO ACTION,
            FOREIGN KEY (dish_id) 
                REFERENCES dish (dish_id) 
                    ON DELETE CASCADE 
                    ON UPDATE NO ACTION,
            FOREIGN KEY (recipe_id) 
                REFERENCES recipe_ingredient (recipe_id) 
                    ON DELETE CASCADE 
                    ON UPDATE NO ACTION,
            FOREIGN KEY (recipe_id) 
                REFERENCES user_favoriate_list (recipe_id) 
                    ON DELETE CASCADE 
                    ON UPDATE NO ACTION
            );""",

        """CREATE TABLE IF NOT EXISTS dish (
            dish_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            dish_type TEXT NOT NULL UNIQUE,
            FOREIGN KEY (dish_id) 
                REFERENCES recipes (dish_id) 
                    ON DELETE CASCADE 
                    ON UPDATE NO ACTION
            );""",

        """CREATE TABLE IF NOT EXISTS category (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            category_name TEXT NOT NULL UNIQUE,
            FOREIGN KEY (category_id) 
                REFERENCES recipes (category_id) 
                    ON DELETE CASCADE 
                    ON UPDATE NO ACTION
            );""",

        """CREATE TABLE IF NOT EXISTS unit (
            unit_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            unit_name TEXT NOT NULL UNIQUE,
            FOREIGN KEY (unit_id) 
                REFERENCES recipe_ingredient (unit) 
                    ON DELETE CASCADE 
                    ON UPDATE NO ACTION
            );""",

        """CREATE TABLE IF NOT EXISTS ingredient (
            ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            ingredient_name TEXT NOT NULL UNIQUE,
            ingredient_type TEXT NOT NULL,
            FOREIGN KEY (ingredient_id) 
                REFERENCES users (food_allergy) 
                    ON DELETE CASCADE 
                    ON UPDATE NO ACTION,
            FOREIGN KEY (ingredient_id)
                REFERENCES recipe_ingredient (ingredient_id) 
                    ON DELETE CASCADE 
                    ON UPDATE NO ACTION
            );""",

        """CREATE TABLE IF NOT EXISTS recipe_ingredient (
            recipe_id INTEGER, 
            ingredient_id INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            unit INTEGER NOT NULL,
            PRIMARY KEY (recipe_id, ingredient_id),
            FOREIGN KEY (unit) 
                REFERENCES unit (unit_id) 
                    ON DELETE CASCADE
                    ON UPDATE NO ACTION,
            FOREIGN KEY (ingredient_id) 
                REFERENCES ingredient (ingredient_id) 
                    ON DELETE CASCADE
                    ON UPDATE NO ACTION
            );""",
    ]

class DatabaseInitialize:

    def __init__(self) -> None:
        self.sql_query:str = ""
        self.cursor = None
        self.recipe_list: list = []
        self.__database_initialize()


    def __connect(self):
        try:
            with sqlite3.connect('recipes.sqlite') as self.conn:
                self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(e)

    def __loading_json_file(self, file_name):
        try:
            with open(file_name) as json_file:
                recipes_data = json.load(json_file)
            self.recipe_list = recipes_data['recipes']
        except FileNotFoundError:
            print("File not found")
        except json.decoder.JSONDecodeError:
            print("Invalid JSON")
        except Exception as e:
            print(e)

    def __database_initialize(self) -> None:
        if not os.path.isfile('recipes.sqlite'):
            self.__connect()
            for statement in CREATE_TABLE_STATEMENTS:
                self.cursor.execute(statement)
                self.conn.commit()
            self.cursor.executemany("INSERT INTO dish (dish_type) VALUES (?)", SERVING_TYPE)
            self.cursor.executemany("INSERT INTO category (category_name) VALUES (?)", DIET_CATEGORY)
            self.cursor.executemany("INSERT INTO unit (unit_name) VALUES (?)", UNIT)
            self.cursor.executemany("INSERT INTO food_type_list (type_name) VALUES (?)", FOOD_TYPE)
            self.cursor.execute("INSERT INTO users (username, password, email, diet_preference, halal_food, admin_account) "
                                "VALUES (?,?,?,?,?,?)", ("admin","1234","admin@recipemanager.co.uk",'Flexitarian (Normal Diet)',
                                                         0,1))
            self.conn.commit()
            self.__loading_json_file("preload_recipes.json")
            self.insert_preload_recipe()
        else:
            self.__connect()


    def insert_preload_recipe(self) -> None:
        for each_recipe in self.recipe_list:
            recipe_name : str = each_recipe['recipe name']
            halal_food: bool = each_recipe['halal food']
            cooking_time: str = each_recipe['cooking time']
            recipe_category: str= each_recipe['recipe category']
            calories_per_serving: int = each_recipe['calories per serving']
            ingredients_list: dict = each_recipe['ingredients']
            instructions_details: str = each_recipe['instructions']
            image_one:str = each_recipe['pictures']['picture one']
            image_two:str = each_recipe['pictures']['picture two']
            image_three:str = each_recipe['pictures']['picture three']

            # Put general recipe information into database (recipe table)
            self.sql_query: str = 'select category_id from category where category_name = ?'
            search_result: list = self.__execute_sql((each_recipe['diet category'].title(),))
            category_id: int = search_result[0][0]
            self.sql_query: str = 'select dish_id from dish where dish_type = ?'
            search_result: list = self.__execute_sql((each_recipe['dish type'].title(),))
            dish_id: int = search_result[0][0]
            self.sql_query = ('insert into recipes (recipe_name, category_id, instructions, image_one, image_two,'
                              'image_three, cooking_time, dish_id, calories_per_serving, is_halal_food,recipe_category)'
                              'values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)')
            self.__execute_insert_query((recipe_name, category_id, instructions_details, image_one, image_two,
                                       image_three, cooking_time, dish_id, calories_per_serving, halal_food,recipe_category))

            for key,value in ingredients_list.items():
                # Check if ingredient exist in database already, if not then add new ingredient into ingredient table.
                self.sql_query = 'select * from ingredient where ingredient_name = ?'
                search_result = self.__execute_sql((key,))
                if len(search_result) == 0:
                    self.sql_query: str = 'select type_id from food_type_list where type_name = ?'
                    search_result: list = self.__execute_sql((value['food type'].title(),))
                    type_id: int = search_result[0][0]
                    self.sql_query = 'insert into ingredient (ingredient_name, ingredient_type) values (?, ?)'
                    self.__execute_insert_query((key, type_id))

            # third part, put all related ingredient into recipe ingredient table
            for key, value in ingredients_list.items():
                recipe_id: int = each_recipe['recipe id']
                unit_name: str = each_recipe['ingredients'][key]['unit'].capitalize()
                self.sql_query = 'select * from ingredient where ingredient_name = ?'
                search_result = self.__execute_sql((key,))
                ingredient_id: int = search_result[0][0]
                self.sql_query = 'select unit_id from unit where unit_name = ?'
                unit_id = self.__execute_sql((unit_name,))
                self.sql_query = 'insert into recipe_ingredient (recipe_id, ingredient_id, amount, unit) values (?, ?, ?, ?)'
                self.__execute_insert_query((recipe_id, ingredient_id, value['amount'], unit_id[0][0]))

    def __execute_sql(self, value) -> list:
        with self.conn:
            return self.cursor.execute(self.sql_query, value).fetchall()

    def __execute_insert_query(self, value) -> None:
        with self.conn:
            self.cursor.execute(self.sql_query, value)

    def __close_connect(self) -> None:
        self.conn.close()