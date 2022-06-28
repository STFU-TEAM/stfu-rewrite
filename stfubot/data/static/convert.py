import json
import os

with open(
    "PATH",
    "r",
) as reader:
    file_stand = json.load(reader)["stand"]
    for stand in file_stand:
        stand["base_damage"] += 25


with open(
    "PATH",
    "w",
) as writer:
    json.dump({"stand": file_stand}, writer)
