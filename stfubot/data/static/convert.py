import json
import os

print(
    os.listdir(
        "C:/Users/EWWWSAMPC/Documents/programmation/StfuRewrite/stfubot/data/static/"
    )
)

with open(
    "C:/Users/EWWWSAMPC/Documents/programmation/StfuRewrite/stfubot/data/static/stand.json",
    "r",
) as item:
    standFile = json.load(item)["stand"]
with open("stand_template.json", "w") as reader:
    dictio = {"stand": []}
    for stand in standFile:
        st = {
            "id": stand["id"],
            "name": stand["stand_name"],
            "stars": stand["stars"],
            "special_description": stand["special"],
            "base_hp": stand["stats"]["base_hp"],
            "base_damage": stand["stats"]["base_damage"],
            "base_speed": stand["stats"]["base_speed"],
            "turn_for_ability": stand["stats"]["turn_for_ability"],
            "base_critical": 1,
        }
        dictio["stand"].append(st)
    json.dump(dictio, reader)
