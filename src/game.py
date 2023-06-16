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
        immune: bool,
        counter: int,
    ) -> None:
        self.player = player
        self.time = time
        self.index = index
        self.records = records
        self.immune = immune
        self.counter = counter

    def start(self):
        max_geode = self.player.materials.get(Type.GEODE, 0)
        """
        code pas fou ici mon on essaie deja de faire marcher le tout
        """
        records2 = self.records[self.index]

        # if (all([records2[key] is not None for key in records2])) and (
        #     all([self.index > records2[key] for key in records2])
        #     and not (self.immune)
        # ):
        #     return max_geode

        records3 = {key: value for key, value in records2.items() if value is not None}
        for key in records3:
            if self.player.materials.get(key) is None:
                print(self.player.materials)
                print(self.index)
                return max_geode

        for i in range(self.index, self.time):
            clone = deepcopy(self.player)
            actions = self.player.get_actions_could_do()
            for action in actions:
                if not (action):
                    # self.immune = True
                    self.player.play(receipt_to_use=action)
                    max_geode = max(max_geode, self.player.materials.get(Type.GEODE, 0))
                    for key in self.player.materials:
                        records = self.records[self.index]
                        if records[key] is None:
                            records[key] = self.index
                            # self.immune = True
                        elif self.index < records[key]:
                            records[key] = self.index
                            self.immune = True
                    self.counter += 1
                else:
                    # self.immune = True
                    clone_player = deepcopy(clone)
                    clone_player.play(receipt_to_use=action)
                    for key in clone_player.materials:
                        records = self.records[self.index]
                        if records[key] is None:
                            records[key] = self.index
                            # self.immune = True
                        elif self.index < records[key]:
                            records[key] = self.index
                            self.immune = True
                    new_game = Game(
                        player=clone_player,
                        time=self.time,
                        index=i + 1,
                        records=self.records,
                        immune=self.immune,
                        counter=0,
                    )
                    max_geode = max(max_geode, new_game.start())
        return max_geode


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
    immune=False,
    counter=0,
)
print(game.start())
end = time.time() - start
print(end)
print(game.records)
