import re

from materials.base_material import Type
from recipe.recipe import Recipe


def parse():
    blueprints = []
    pattern = (
        r"Each (\w+) robot costs (\d+) (\w+)(?:, (\d+) (\w+))?(?: and (\d+) (\w+))?"
    )

    with open("blueprints.txt", "r") as file:
        blueprints = []
        for line in file:
            blueprint = []
            for robot in line.split("."):
                match = re.match(pattern, robot.strip())
                if not (match):
                    break
                robot_type, *cost_resource_pairs = match.groups()
                for i in range(0, len(cost_resource_pairs), 2):
                    cost = cost_resource_pairs[i]
                    resource = cost_resource_pairs[i + 1]
                    if cost and resource:
                        resource = resource[:-1] if resource.endswith("s") else resource
                        blueprint.append(
                            Recipe(
                                robot_type=search_enum(robot_type),
                                needs={search_enum(resource): int(cost)},
                                productivity=1,
                            )
                        )
            blueprints.append(blueprint)
    return blueprints


def search_enum(resource: str):
    for key in Type:
        if key.value == resource:
            return key
    return None
