from materials.base_material import Type


class BaseRobot:
    def __init__(self, type: Type, productivity: int) -> None:
        self.type = type
        self.productivity = productivity

    def farm(self) -> int:
        return self.productivity
