from copy import deepcopy

from materials.base_material import Type
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
        max_geodes: int,
    ) -> None:
        self.player = player
        self.duration = duration
        self.index = index
        self.records = records
        self.max_geodes = max_geodes

    def start(self):
        if not (self.__validate_records()):
            return self.max_geodes
        for i in range(self.index, self.duration):
            self.index = i
            self.__process_actions()
        return self.max_geodes

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
        self.max_geodes = max(self.max_geodes, self.player.materials.get(Type.GEODE, 0))
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
            max_geodes=self.max_geodes,
        )
        return max(self.max_geodes, new_game.start())


limits = {
    Type.ORE: 1,
    Type.CLAY: 4,
    Type.OBSIDIAN: 2,
    Type.GEODE: 2,
}

recipes = [
    Recipe(robot_type=Type.ORE, needs={Type.ORE: 4}, productivity=1),
    Recipe(robot_type=Type.CLAY, needs={Type.ORE: 2}, productivity=1),
    Recipe(
        robot_type=Type.OBSIDIAN, needs={Type.ORE: 3, Type.CLAY: 14}, productivity=1
    ),
    Recipe(
        robot_type=Type.GEODE, needs={Type.ORE: 2, Type.OBSIDIAN: 7}, productivity=1
    ),
]

player = Player(
    materials={},
    robots=[BaseRobot(type=Type.ORE, productivity=1)],
    recipes=recipes,
    limits=limits,
)
import time

start = time.time()
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
        }
    ]
    * 25,
    max_geodes=0,
)
print(game.start())
end = time.time() - start
print(end)
print(game.records)
