from player.player import Player
from copy import deepcopy
from materials.base_material import Type
from receipts.receipt import Receipt
from robots.base_robot import BaseRobot


class Game:
    def __init__(
        self,
        player: Player,
        time: int,
        index: int,
        records: dict,
        max_geodes: int,
    ) -> None:
        self.player = player
        self.time = time
        self.index = index
        self.records = records
        self.max_geodes = max_geodes

    def start(self):
        for i in range(self.index, self.time):
            self.index = i
            actions = self.player.get_actions_could_do()
            self.__process_actions(actions=actions)
        return self.max_geodes

    def __process_actions(self, actions: list) -> None:
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
        self.player.play(receipt_to_use=None)
        self.max_geodes = max(self.max_geodes, self.player.materials.get(Type.GEODE, 0))
        self.__save_to_records(materials=self.player.materials)

    def __play_action(self, action: Receipt, actual_player: Player):
        clone_player = deepcopy(actual_player)
        clone_player.play(receipt_to_use=action)
        self.__save_to_records(materials=clone_player.materials)
        self.__create_new_game_and_get_max_geodes(new_player=clone_player)

    def __create_new_game_and_get_max_geodes(self, new_player: Player) -> int:
        new_game = Game(
            player=new_player,
            time=self.time,
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

receipts = [
    Receipt(robot_type=Type.ORE, needs={Type.ORE: 4}, productivity=1),
    Receipt(robot_type=Type.CLAY, needs={Type.ORE: 2}, productivity=1),
    Receipt(
        robot_type=Type.OBSIDIAN, needs={Type.ORE: 3, Type.CLAY: 14}, productivity=1
    ),
    Receipt(
        robot_type=Type.GEODE, needs={Type.ORE: 2, Type.OBSIDIAN: 7}, productivity=1
    ),
]

player = Player(
    materials={},
    robots=[BaseRobot(type=Type.ORE, productivity=1)],
    receipts=receipts,
    limits=limits,
)
import time

start = time.time()
game = Game(
    player=player,
    time=24,
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
