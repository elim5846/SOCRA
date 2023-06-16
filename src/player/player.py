from receipts.receipt import Receipt
from robots.base_robot import BaseRobot


class Player:
    def __init__(
        self, materials: dict, robots: list, receipts: list, limits: dict
    ) -> None:
        self.materials = materials
        self.robots = robots
        self.limits = limits
        self.receipts = receipts

    def play(self, receipt_to_use: None | Receipt) -> None:
        if receipt_to_use and self.__should_use_receipt(receipt=receipt_to_use):
            robot = self.__craft_robot(receipt=receipt_to_use)
            self.__use_robots()
            self.robots.append(robot)
        else:
            self.__use_robots()

    def get_actions_could_do(self) -> list:
        actions_could_do = [None]
        for receipt in self.receipts:
            if self.__should_use_receipt(receipt=receipt):
                actions_could_do.append(receipt)
        return actions_could_do

    def __use_robots(self) -> None:
        for robot in self.robots:
            self.materials[robot.type] = self.materials.get(robot.type, 0)
            self.materials[robot.type] += robot.productivity

    def __should_use_receipt(self, receipt: Receipt) -> bool:
        return self.__can_craft(receipt=receipt) and self.__should_craft(
            receipt=receipt
        )

    def __should_craft(self, receipt: Receipt) -> bool:
        nb_receipt_robot_in_stock = len(
            [robot for robot in self.robots if robot.type == receipt.robot_type]
        )
        return self.limits[receipt.robot_type] > nb_receipt_robot_in_stock

    def __can_craft(self, receipt: Receipt) -> bool:
        for key, value in receipt.needs.items():
            if value > self.materials.get(key, 0):
                return False
        return True

    def __craft_robot(self, receipt: Receipt) -> BaseRobot:
        for key, value in receipt.needs.items():
            self.materials[key] -= value
        return BaseRobot(type=receipt.robot_type, productivity=receipt.productivity)
