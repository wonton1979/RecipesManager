from ingredient import Ingredient


class Recipe:
    __recipes_created = 0
    VEGAN_EXCLUDE_INGREDIENTS = ['Meat','Poultry','Seafood','Egg','Dairy Products']
    LACTO_VEGETARIAN_EXCLUDE_INGREDIENTS = ['Meat','Poultry','Seafood','Dairy Products']
    OVO_VEGETARIAN_EXCLUDE_INGREDIENTS = ['Meat', 'Poultry', 'Seafood', 'Egg']
    def __init__(self, name:str, description:str, ingredients:list,cuisine:str) -> None:
        self.name = name
        self.description = description
        self.ingredients = ingredients
        self.cuisine = cuisine
        self.total_calories = self.__total_calories()
        self.total_cost = self.__total_cost()
        Recipe.__recipes_created += 1

    @staticmethod
    def get_recipes_created():
        return Recipe.__recipes_created


    def check_if_vegan_recipes(self) -> bool:
        for ingredient in self.ingredients:
            if ingredient[0].ingredient_type in Recipe.VEGAN_EXCLUDE_INGREDIENTS:
                return False
        return True

    def check_if_lacto_vegetarian_recipes(self) -> bool:
        for ingredient in self.ingredients:
            if ingredient[0].ingredient_type in Recipe.LACTO_VEGETARIAN_EXCLUDE_INGREDIENTS:
                return False
        return True

    def check_if_ovo_vegetarian_recipes(self) -> bool:
        for ingredient in self.ingredients:
            if ingredient[0].ingredient_type in Recipe.OVO_VEGETARIAN_EXCLUDE_INGREDIENTS:
                return False
        return True

    def __total_calories(self) -> float:
        total_calories = 0
        for ingredient in self.ingredients:
            total_calories += ingredient[0].calories_per_hundred_grams * ingredient[1]/100
        return total_calories

    def __total_cost(self) -> float:
        total_cost = 0
        for ingredient in self.ingredients:
            total_cost += ingredient[0].price_per_hundred_grams * ingredient[1]/100
        return total_cost
