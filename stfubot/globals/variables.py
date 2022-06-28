import asyncio

# URL

CRUSADEURL = "https://c.tenor.com/Qp2FQMOC0HMAAAAC/jotaro-kujo-joseph-joestar.gif"

# Bot loop

LOOP = asyncio.get_event_loop()

# Stand Scaling

STXPTOLEVEL = 1000
HPSCALING = 5
SPEEDSCALING = 1
DAMAGESCALING = 5
CRITICALSCALING = 0.5
CRITMULTIPLIER = 1.5
DODGENERF = 10

# Fight Rewards

COINSGAINS = 300
PLAYER_XPGAINS = 10
STAND_XPGAINS = 10


# User scalings

USRXPTOLEVEL = 1000

# Crusade Items

CHANCEITEM = 10
DONOR_CR_WAIT_TIME = 1
NORMAL_CR_WAIT_TIME = 1.5

# Tower constants

ENTRYCOST = 500
TOWERURL = "https://storage.stfurequiem.com/randomAsset/tower.png"

# ADV

DONOR_ADV_WAIT_TIME = 6
NORMAL_ADV_WAIT_TIME = 6

# Shop

SHOPCREATIONCOST = 3000

ITEMTYPE = ["damage", "utility", "stand", "misc"]
ITEMBYTYPE = {
    "damage": [{"id": 1}, {"id": 5}],
    "utility": [{"id": 6}, {"id": 7}],
    "stand": [{"id": 2}, {"id": 8}, {"id": 9}, {"id": 10}, {"id": 11}, {"id": 12}],
    "misc": [{"id": 3}, {"id": 13}],
}

# Gang

GANGURL = "https://storage.stfurequiem.com/randomAsset/gang_default.jpg"
GANGCREATIONCOST = 50000

# Vote

ARROW_VOTE = 3
COINS_VOTE = 250
