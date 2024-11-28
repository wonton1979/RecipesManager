class Ingredient:
    __total_ingredients = 0
    def __init__(self, name:str, ingredient_type:str,calories_per_hundred_grams:float, price_per_hundred_grams:float) -> None:
        self.name = name
        self.ingredient_type = ingredient_type
        self.calories_per_hundred_grams = calories_per_hundred_grams
        self.price_per_hundred_grams = price_per_hundred_grams
        Ingredient.__total_ingredients += 1

    @staticmethod
    def get_total_ingredients() -> int:
        return Ingredient.__total_ingredients