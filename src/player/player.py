from recipe.recipe import Recipe
from robots.base_robot import BaseRobot


class Player:
    def __init__(
        self, materials: dict, robots: list, recipes: list, limits: dict
    ) -> None:
        self.materials = materials
        self.robots = robots
        self.limits = limits
        self.recipes = recipes

    def play(self, recipe_to_use: None | Recipe) -> None:
        if recipe_to_use and self.__should_use_recipe(recipe=recipe_to_use):
            robot = self.__craft_robot(recipe=recipe_to_use)
            self.__use_robots()
            self.robots.append(robot)
        else:
            self.__use_robots()

    def get_actions_could_do(self) -> list:
        actions_could_do = [None]
        for recipe in self.recipes:
            if self.__should_use_recipe(recipe=recipe):
                actions_could_do.append(recipe)
        return actions_could_do

    def __use_robots(self) -> None:
        for robot in self.robots:
            self.materials[robot.type] = self.materials.get(robot.type, 0)
            self.materials[robot.type] += robot.productivity

    def __should_use_recipe(self, recipe: Recipe) -> bool:
        return self.__can_craft(recipe=recipe) and self.__should_craft(recipe=recipe)

    def __should_craft(self, recipe: Recipe) -> bool:
        nb_recipe_robot_in_stock = len(
            [robot for robot in self.robots if robot.type == recipe.robot_type]
        )
        return self.limits[recipe.robot_type] > nb_recipe_robot_in_stock

    def __can_craft(self, recipe: Recipe) -> bool:
        for key, value in recipe.needs.items():
            if value > self.materials.get(key, 0):
                return False
        return True

    def __craft_robot(self, recipe: Recipe) -> BaseRobot:
        for key, value in recipe.needs.items():
            self.materials[key] -= value
        return BaseRobot(type=recipe.robot_type, productivity=recipe.productivity)
