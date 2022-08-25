import asyncio

# URL

CRUSADEURL = "https://c.tenor.com/Qp2FQMOC0HMAAAAC/jotaro-kujo-joseph-joestar.gif"
TOWERURL = "https://storage.stfurequiem.com/randomAsset/tower.png"
GANGURL = "https://storage.stfurequiem.com/randomAsset/gang_default.jpg"

# Bot loop

LOOP = asyncio.get_event_loop()

# Stand Scaling

STXPTOLEVEL = 100
LEVEL_TO_STAT_INCREASE = 5
HPSCALING = 2
SPEEDSCALING = 10
DAMAGESCALING = 5
CRITICALSCALING = 50
CRITMULTIPLIER = 1.5
DODGENERF = 10
MAX_LEVEL = 100


# Fight Rewards

COINSGAINS = 300
PLAYER_XPGAINS = 10
STAND_XPGAINS = 50


# User scalings

USRXPTOLEVEL = 1000

# Crusade Items

CHANCEITEM = 10
DONOR_CR_WAIT_TIME = 1
NORMAL_CR_WAIT_TIME = 1.5

# Tower constants

ENTRYCOST = 500

# ADV

DONOR_ADV_WAIT_TIME = 6
NORMAL_ADV_WAIT_TIME = 6

# Shop

SHOPCREATIONCOST = 3000

ITEMTYPE = [
    "damage",
    "utility",
    "stand",
    "part3chips",
    "part4chips",
    "part5chips",
    "misc",
]
ITEMBYTYPE = {
    "damage": [{"id": 1}, {"id": 5}],
    "utility": [{"id": 6}, {"id": 7}],
    "part3chips": [{"id": 9}, {"id": 10}, {"id": 11}, {"id": 12}, {"id": 14}],
    "part4chips": [
        {"id": 17},
        {"id": 18},
        {"id": 19},
        {"id": 20},
        {"id": 21},
        {"id": 22},
        {"id": 23},
    ],
    "part5chips": [
        {"id": 24},
        {"id": 25},
        {"id": 26},
        {"id": 27},
        {"id": 28},
        {"id": 29},
        {"id": 30},
        {"id": 31},
        {"id": 32},
    ],
    "stand": [{"id": 2}, {"id": 8}],
    "misc": [{"id": 3}, {"id": 13}],
}

# Gang

GANGCREATIONCOST = 10000

# Vote

ARROW_VOTE = 3
COINS_VOTE = 250
