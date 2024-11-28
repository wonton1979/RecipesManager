class User:
    __total_users = 0
    def __init__(self, username:str, password:str, email:str, halal_food:bool, food_allergy:list) -> None:
        self.username = username
        self.password = password
        self.email = email
        self.halal_food = halal_food
        self.food_allergy = food_allergy
        User.__total_users += 1


    @staticmethod
    def get_total_users() -> int:
        return User.__total_users
