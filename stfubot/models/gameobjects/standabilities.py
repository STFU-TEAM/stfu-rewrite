import random


from typing import TYPE_CHECKING, List


from stfubot.models.gameobjects.effects import Effect, EffectType

# It's for typehint
if TYPE_CHECKING:
    from stfubot.models.gameobjects.stands import Stand


def get_payload():
    return {
        "gold_experience_requiem": False,
        "tusk_act_4": False,
        "king_crimson": False,
    }


"""

name your fonction to the stand

def special_boiler_plate(stand:"Stand",allied_stand:List["Stand"],ennemy_stand:List["Stand"])->tuple:
    payload = get_payload()
    #Whatever your code does to the lists above
    #Payload Contain behavior change to the game
    #message is what should be printed to the embed
    return payload,message

their is a load of exemple bellow
AOE attack : the_world
AOE effect : weather_report
self buff  : made_in_heaven

"""


def the_world_over_heaven(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    damage = 0
    for ennemy in ennemy_stand:
        damage += stand.attack(ennemy)
    message = f"｢{stand.name}｣! damaged everyone for {int(damage)}!"
    return payload, message


def star_platinum(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = random.randint(1, 4)
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    if len(valid_stand) != 0:
        target: Stand = random.choice(valid_stand)
        stand.attack(target, multiplier=multiplier)
        message = f"｢{stand.name}｣ punches, {target.name}, {multiplier} times dealing {stand.current_damage*multiplier}!"
    else:
        message = f"｢{stand.name}｣ punches multiple times!"
    return payload, message


def silver_chariot(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    stand.current_speed += 10
    stand.ressistance *= 0.75
    message = f"｢{stand.name}｣ gains speed but loses resistance."
    return payload, message


def the_world(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 0.6
    damage = 0
    for ennemy in ennemy_stand:
        damage += stand.attack(ennemy, multiplier=multiplier)
    message = f"｢{stand.name}｣ STOPS TIME! and damages everyone for {int(damage)}"
    return payload, message


def cream(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    stand.current_speed += 5
    stand.current_damage += 5
    stand.effects.append(Effect(EffectType.STUN, 1, 0))
    message = f"｢{stand.name}｣ gets faster"
    return payload, message


def star_platinum_the_world(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 0.6
    damage = 0
    for ennemy in ennemy_stand:
        damage += stand.attack(ennemy, multiplier=multiplier)
    message = f"｢{stand.name}｣ STOPS TIME! and damages everyone for {int(damage)}"
    return payload, message


def crazy_diamond(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    valid_stand = [i for i in allied_stand if i.is_alive() and i != stand]
    if len(valid_stand) != 0:
        ally: "Stand" = random.choice(valid_stand)
        dif_damage = abs(stand.start_hp - stand.current_hp)
        heal = min(ally.start_hp, ally.current_hp + (dif_damage // 2))
        ally.current_hp = heal
        message = f"｢{stand.name}｣ heals {ally.name}"
    else:
        message = f"｢{stand.name}｣ enraged!"
    return payload, message


def the_hand(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    multiplier = random.choice((0.75, 1, 1.5, 2.5))
    payload = get_payload()
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    if len(valid_stand) != 0:
        target: "Stand" = random.choice(valid_stand)
        damage = stand.attack(target, multipler=multiplier)
        message = f"｢{stand.name}｣ throws out random items and deals {damage} damage"
    return payload, message


def heavens_door(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplicator = 2
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    if len(valid_stand) != 0:
        target: "Stand" = random.choice(valid_stand)
        target.effects.append(Effect(EffectType.STUN, multiplicator, 0))
        message = f"｢{stand.name}｣ stuns {target.name} for {multiplicator} rounds!"
    else:
        message = f"｢{stand.name}｣!"
    return payload, message


def killer_queen(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplicator = 1.5
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    if len(valid_stand) != 0:
        target: "Stand" = random.choice(valid_stand)
        target.effects.append(
            Effect(EffectType.POISON, 1, multiplicator * stand.current_damage)
        )
        message = f"｢{stand.name}｣ place a bomb on {target.name} for {multiplicator*stand.current_damage} damage !"
    else:
        message = f"｢{stand.name}｣!"
    return payload, message


def echoes_act_3(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplicator = 2
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    if len(valid_stand) != 0:
        target: "Stand" = random.choice(valid_stand)
        target.effects.append(Effect(EffectType.STUN, multiplicator, 0))
        message = f"｢{stand.name}｣ stuns {target.name} for {multiplicator} rounds"
    else:
        message = f"｢{stand.name}｣!"
    return payload, message


def killer_queen_bite_the_dust(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    heal = (stand.start_hp - stand.current_hp) // 3
    stand.current_hp += heal
    stand.current_hp = max(0, min(stand.current_hp, stand.start_hp))
    message = f"｢{stand.name}｣ resets the timeline! and heals for {heal}"
    return payload, message


def gold_experience(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    multiplier = 30
    payload = get_payload()
    for allies in allied_stand:
        if allies.current_hp < allies.start_hp:
            allies.current_hp += 30
            allies.current_hp = min(allies.start_hp, allies.current_hp)
    message = f"｢{stand.name}｣ heals it's ally for {multiplier}"
    return payload, message


def sticky_finger(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    stand.current_critical += 5
    message = f"｢{stand.name}｣ becomes more precise."
    return payload, message


def purple_haze(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    multiplier = 0.5
    payload = get_payload()
    for s in allied_stand + ennemy_stand:
        s.effects.append(
            Effect(EffectType.POISON, 3, stand.current_damage * multiplier)
        )
    message = f"｢{stand.name}｣ poisons everyone for {stand.current_damage*multiplier}!"
    return payload, message


def king_crimson(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    payload["king_crimson"] = True
    message = f"｢{stand.name}｣ has already..."
    return payload, message


def notorious_big(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    multiplier = 0.1
    payload = get_payload()
    alive_allies = [i for i in allied_stand if i.is_alive() and i != stand]
    if len(alive_allies) != 0:
        stand.effects.append(
            Effect(EffectType.REGENERATION, 1, stand.current_hp * multiplier)
        )
    message = f"｢{stand.name}｣ Regenerates itself!"
    return payload, message


def metallica(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    multiplier = 0.5
    payload = get_payload()
    for ennemy in ennemy_stand:
        for effect in ennemy.effects:
            if effect == EffectType.REGENERATION:
                effect.value *= multiplier
        ennemy.effects.append(Effect(EffectType.POISON, 2, stand.current_damage * 0.1))
    message = f"｢{stand.name}｣ infects their blood stream!"
    return payload, message


def green_day(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    multiplier = 0.90
    payload = get_payload()
    for ennemy in ennemy_stand:
        ennemy.effects.append(Effect(EffectType.WEAKEN, 3, multiplier))
    message = f"｢{stand.name}｣ weakens all enemies!"
    return payload, message


def chariot_requiem(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    if len(valid_stand) != 0:
        target: "Stand" = random.choice(valid_stand)
        if target.id != stand.id:
            return specials[f"{target.id}"](stand, allied_stand, ennemy_stand)
    stand.current_damage += 5
    message = f"｢{stand.name}｣'s soul searches for the arrow..."
    return payload, message


def gold_experience_requiem(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    payload["GER"] = True
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    message = f"｢{stand.name}｣ You will never reach the truth, Return to Zero!"
    # reset their scaling
    for ennemy in ennemy_stand:
        ennemy: "Stand" = stand
        ennemy.current_hp = min(ennemy.current_hp, ennemy.start_hp)
        ennemy.current_damage = min(ennemy.current_damage, ennemy.start_damage)
        ennemy.current_speed = min(ennemy.current_speed, ennemy.start_speed)
    if len(valid_stand) != 0:
        target = random.choice(valid_stand)
        target.effects.append(Effect(EffectType.STUN, 2, 0))
        message += f"｢{stand.name}｣ stunned {target.name}!"
    return payload, message


def stone_free(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    multiplier = 0.90
    payload = get_payload()
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    message = f"｢{stand.name}｣ frees the stone ocean!"
    if len(valid_stand) != 0:
        target = random.choice(valid_stand)
        target.effects.append(Effect(EffectType.STUN, 1, 0))
        target.current_speed *= multiplier
    return payload, message


def weather_report(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 0.20
    for ennemy in ennemy_stand:
        ennemy.effects.append(
            Effect(EffectType.POISON, 3, stand.current_damage * multiplier)
        )
    message = f"｢{stand.name}｣ makes death rain... and poisons everyone for {stand.current_damage*multiplier}!"
    return payload, message


def jumpin_jack_flash(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    message = f"｢{stand.name}｣ removes gravity!"
    if len(valid_stand) != 0:
        target = random.choice(valid_stand)
        target.effects.append(Effect(EffectType.STUN, stand.turn // 2, 0))
    return payload, message


def bohemian_rhapsody(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    message = f"｢{stand.name}｣ creates a perfect version of itself!"
    for ally in allied_stand:
        stand.current_hp = max(stand.current_hp, ally.current_hp)
        stand.current_damage = max(stand.current_damage, ally.current_damage)
        stand.current_critical = max(stand.current_critical, ally.current_critical)
        stand.current_speed = max(stand.current_speed, ally.current_speed)
    return payload, message


def underworld(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    multiplier = 4
    payload = get_payload()
    if sum([s.is_alive() for s in allied_stand]) == len(allied_stand):
        message = f"｢{stand.name}｣ waits for an ally to die..."
        stand.special_meter = 2
        return payload, message
    valid_stand = [i for i in ennemy_stand if not i.is_alive()]
    revived = random.choice(valid_stand)
    revived.current_hp = revived.start_hp // 4
    message = f"｢{stand.name}｣ brings a memory of {revived.name}!"
    return payload, message


def c_moon(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    for ennemy in ennemy_stand:
        ennemy.current_speed -= 2
    message = f"｢{stand.name}｣ alters the gravity!"
    return payload, message


def made_in_heaven(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    stand.current_speed += 5
    stand.current_damage += 20
    stand.current_critical += 5
    message = f"｢{stand.name}｣'s speed increases!"
    return payload, message


def tusk_act_4(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 0.75
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    message = f"｢{stand.name}｣ lesson  5!"
    if len(valid_stand) != 0:
        target = random.choice(valid_stand)
        target.effects.append(
            Effect(EffectType.POISON, 4, multiplier * stand.current_damage)
        )
        message += f" damage ｢{target.name}｣ for {stand.current_damage*multiplier} for 4 rounds"
    return payload, message


def ball_breaker(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 0.65
    for ennemy in ennemy_stand:
        ennemy.effects.append(Effect(EffectType.WEAKEN, 1, multiplier))
    for ally in allied_stand:
        ally.current_damage += 5
    message = f"｢{stand.name}｣ harnesses the power of the spin!"
    return payload, message


def dirty_deed_done_dirt_cheap(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    stand.effects = [e for e in stand.effects if e.type == EffectType.REGENERATION]
    message = f"｢{stand.name}｣ retrieves an alternate version!"
    return payload, message


def boku_no_rythm_wo_kiitekure(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    multiplicator = 0.5
    payload = get_payload()
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    for target in valid_stand:
        target: "Stand" = random.choice(valid_stand)
        target.effects.append(
            Effect(EffectType.POISON, 1, multiplicator * stand.current_damage)
        )
    message = f"｢{stand.name}｣ plants bombs on everyone."
    return payload, message


def mandom(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    for ally in allied_stand:
        ally.current_critical += 5
    message = f"Welcome to the True Man's world!"
    return payload, message


def the_world_sbr(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 0.6
    damage = 0
    for ennemy in ennemy_stand:
        damage += stand.attack(ennemy, multiplier=multiplier)["damage"]
    message = f"｢{stand.name}｣ STOPS TIME! and damages everyone for {int(damage)}"
    return payload, message


def soft_and_wet(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    multiplier = 0.50
    payload = get_payload()
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    message = f"｢{stand.name}｣ breaks and weakens!"
    if len(valid_stand) != 0:
        target = random.choice(valid_stand)
        target.effects.append(Effect(EffectType.WEAKEN, 1, multiplier))
    return payload, message


def doobie_wah(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 0.1
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    message = f"｢{stand.name}｣ seeks it's enemy!"
    if len(valid_stand) != 0:
        target = random.choice(valid_stand)
        target.effects.append(
            Effect(EffectType.POISON, 1, multiplier * stand.current_damage)
        )
    return payload, message


def walking_heart(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    stand.current_damage += 5
    stand.current_critical += 1
    message = f"｢{stand.name}｣ !"
    return payload, message


def wonder_of_u(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplicator = 0.1
    dif_damage = abs(stand.start_hp - stand.current_hp)
    woudamage = lambda speed: speed * (dif_damage * speed * multiplicator) ** (1 / 2)
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    message = f"｢{stand.name}｣ !"
    if len(valid_stand) != 0:
        target = random.choice(valid_stand)
        target.current_hp -= woudamage(stand.current_speed)
        message = f"｢{stand.name}｣ redirects calamity to {target.name} for {woudamage(stand.current_speed)}!"
    return payload, message


def victorious_star_platinum(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 0.4
    damage = 0
    for ennemy in ennemy_stand:
        damage += stand.attack(ennemy, multiplier=multiplier)
    message = f"｢{stand.name}｣ STOPS TIME! and damages everyone for {int(damage)}"
    return payload, message


specials = {
    "1": star_platinum,
    "6": silver_chariot,
    "10": the_world,
    "30": cream,
    "31": star_platinum_the_world,
    "32": crazy_diamond,
    "34": the_hand,
    "45": heavens_door,
    "49": killer_queen,
    "50": echoes_act_3,
    "58": killer_queen_bite_the_dust,
    "59": gold_experience,
    "60": sticky_finger,
    "69": purple_haze,
    "75": king_crimson,
    "78": notorious_big,
    "80": metallica,
    "81": green_day,
    "83": chariot_requiem,
    "84": gold_experience_requiem,
    "86": stone_free,
    "94": weather_report,
    "95": jumpin_jack_flash,
    "103": bohemian_rhapsody,
    "105": underworld,
    "108": c_moon,
    "109": made_in_heaven,
    "114": tusk_act_4,
    "115": ball_breaker,
    "120": dirty_deed_done_dirt_cheap,
    "124": boku_no_rythm_wo_kiitekure,
    "126": mandom,
    "134": the_world_sbr,
    "137": soft_and_wet,
    "149": doobie_wah,
    "154": walking_heart,
    "161": wonder_of_u,
    "163": victorious_star_platinum,
}
