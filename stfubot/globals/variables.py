import asyncio

# URL

CRUSADEURL = "https://c.tenor.com/Qp2FQMOC0HMAAAAC/jotaro-kujo-joseph-joestar.gif"

# Bot loop

LOOP = asyncio.get_event_loop()

# Stand Scaling

STXPTOLEVEL = 100
XPRATE = 0.1
HPSCALING = 50
SPEEDSCALING = 1
DAMAGESCALING = 5
CRITICALSCALING = 0.5
CRITMULTIPLIER = 1.25
DODGENERF = 10

# Fight Rewards

COINSGAINS = 300
PLAYER_XPGAINS = 10
STAND_XPGAINS = 10


# User scalings

USRXPTOLEVEL = 100

# Crusade Items

CHANCEITEM = 25

# Tower constants

ENTRYCOST = 100
TOWERURL = "https://storage.stfurequiem.com/randomAsset/tower.png"

# Shop

SHOPCREATIONCOST = 1500

ITEMTYPE = ["damage", "utility", "stand", "misc"]
ITEMBYTYPE = {
    "damage": [{"id": 1}, {"id": 5}],
    "utility": [{"id": 6}, {"id": 7}],
    "stand": [{"id": 2}, {"id": 8}, {"id": 9}, {"id": 10}, {"id": 11}, {"id": 12}],
    "misc": [{"id": 3}, {"id": 13}],
}
