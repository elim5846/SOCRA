class Recipe:
    def __init__(self, robot_type: str, needs: dict, productivity: int) -> None:
        self.robot_type = robot_type
        self.needs = needs
        self.productivity = productivity
