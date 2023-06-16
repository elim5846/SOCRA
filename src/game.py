import re
import time
from copy import deepcopy

from materials.base_material import Type
from parse import parse
from player.player import Player
from recipe.recipe import Recipe
from robots.base_robot import BaseRobot


class Game:
    def __init__(
        self,
        player: Player,
        duration: int,
        index: int,
        records: dict,
        max_diamonds: int,
    ) -> None:
        self.player = player
        self.duration = duration
        self.index = index
        self.records = records
        self.max_diamonds = max_diamonds

    def start(self):
        if not (self.__validate_records()):
            return self.max_diamonds
        for i in range(self.index, self.duration):
            self.index = i
            self.__process_actions()
        return self.max_diamonds

    def __validate_records(self) -> bool:
        for key, value in self.records[self.index].items():
            if value and self.player.materials.get(key) is None:
                return False
        return True

    def __process_actions(self) -> None:
        actions = self.player.get_actions_could_do()
        for action in actions:
            actual_player_state = deepcopy(self.player)
            if not (action):
                self.__play_no_action()
            else:
                self.__play_action(action=action, actual_player=actual_player_state)

    def __save_to_records(self, materials: dict):
        for key in materials:
            records = self.records[self.index]
            if records[key] is None or self.index < records[key]:
                records[key] = self.index

    def __play_no_action(self):
        self.player.play(recipe_to_use=None)
        self.max_diamonds = max(
            self.max_diamonds, self.player.materials.get(Type.DIAMOND, 0)
        )
        self.__save_to_records(materials=self.player.materials)

    def __play_action(self, action: Recipe, actual_player: Player):
        clone_player = deepcopy(actual_player)
        clone_player.play(recipe_to_use=action)
        self.__save_to_records(materials=clone_player.materials)
        self.__create_new_game_and_get_max_geodes(new_player=clone_player)

    def __create_new_game_and_get_max_geodes(self, new_player: Player) -> int:
        new_game = Game(
            player=new_player,
            duration=self.duration,
            index=self.index + 1,
            records=self.records,
            max_diamonds=self.max_diamonds,
        )
        return max(self.max_diamonds, new_game.start())


def find_limits(recipes: list) -> dict:
    limits = {}
    for recipe in recipes:
        for key, value in recipe.needs.items():
            limits[key] = max(limits.get(key, 0), value)
    limits[Type.DIAMOND] = 4
    return limits


if __name__ == "__main__":
    recipes = parse()
    results = {}
    for index in range(len(recipes)):
        recipe = recipes[index]
        limits = find_limits(recipes=recipe)
        player = Player(
            materials={},
            robots=[BaseRobot(type=Type.ORE, productivity=1)],
            recipes=recipes[1],
            limits=limits,
        )
        game = Game(
            player=player,
            duration=24,
            index=0,
            records=[
                {
                    Type.ORE: None,
                    Type.CLAY: None,
                    Type.OBSIDIAN: None,
                    Type.GEODE: None,
                    Type.DIAMOND: None,
                }
            ]
            * 25,
            max_diamonds=0,
        )
        max_diamonds = game.start()
        results[f"Blueprint {index + 1}"] = max_diamonds
    f = open("analysis.txt", "w")
    for key, value in results.items():
        f.write(f"{key}: {value}\n")
    max_value = list(results.values()).index(max(results.values()))
    f.write(f"Best blueprint is the blueprint {max_value + 1}.\n")
    f.close()
