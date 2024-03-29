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
        "is_a_special": True,
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
        damage += stand.attack(ennemy, multiplier=1000)["damage"]
    message = f"｢{stand.name}｣! damaged everyone for {int(damage)}!"
    return payload, message


def star_platinum(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = random.randint(1, 4)
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    if len(valid_stand) != 0:
        target: "Stand" = random.choice(valid_stand)
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
        damage += stand.attack(ennemy, multiplier=multiplier)["damage"]
    message = f"｢{stand.name}｣ STOPS TIME! and damages everyone for {int(damage)}"
    return payload, message


def cream(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    stand.current_speed += 5
    stand.current_damage += 5
    stand.effects.append(Effect(EffectType.STUN, 1, 0, stand))
    message = f"｢{stand.name}｣ gets faster"
    return payload, message


def star_platinum_the_world(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 0.6
    damage = 0
    for ennemy in ennemy_stand:
        damage += stand.attack(ennemy, multiplier=multiplier)["damage"]
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
    message = f"｢{stand.name}｣ !"
    if len(valid_stand) != 0:
        target: "Stand" = random.choice(valid_stand)
        damage = stand.attack(target, multiplier=multiplier)
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
        target.effects.append(Effect(EffectType.STUN, multiplicator, 0, stand))
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
            Effect(EffectType.POISON, 1, multiplicator * stand.current_damage, stand)
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
        target.effects.append(Effect(EffectType.STUN, multiplicator, 0, stand))
        message = f"｢{stand.name}｣ stuns {target.name} for {multiplicator} rounds and slow everyone else"
        for st in valid_stand:
            if st != target:
                st.effects.append(Effect(EffectType.SLOW, 2, 10, stand))
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
            Effect(EffectType.POISON, 3, stand.current_damage * multiplier, stand)
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
            Effect(EffectType.REGENERATION, 1, stand.current_hp * multiplier, stand)
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
        ennemy.effects.append(
            Effect(EffectType.POISON, 2, stand.current_damage * 0.1, stand)
        )
    message = f"｢{stand.name}｣ infects their blood stream!"
    return payload, message


def green_day(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    multiplier = 0.90
    payload = get_payload()
    for ennemy in ennemy_stand:
        ennemy.effects.append(Effect(EffectType.WEAKEN, 3, multiplier, stand))
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
            try:
                return specials[f"{target.id}"](stand, allied_stand, ennemy_stand)
            except:
                stand.current_damage += 10
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
        target.effects.append(Effect(EffectType.STUN, 2, 0, stand))
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
        target.effects.append(Effect(EffectType.STUN, 1, 0, stand))
        target.current_speed *= multiplier
    return payload, message


def weather_report(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 0.20
    for ennemy in ennemy_stand:
        ennemy.effects.append(
            Effect(EffectType.POISON, 3, stand.current_damage * multiplier, stand)
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
        target.effects.append(Effect(EffectType.STUN, stand.turn // 2, 0, stand))
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
    valid_stand = [i for i in allied_stand if not i.is_alive()]
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
            Effect(EffectType.POISON, 4, multiplier * stand.current_damage, stand)
        )
        message += f" damage ｢{target.name}｣ for {stand.current_damage*multiplier} for 4 rounds"
    return payload, message


def ball_breaker(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 0.65
    for ennemy in ennemy_stand:
        ennemy.effects.append(Effect(EffectType.WEAKEN, 1, multiplier, stand))
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
            Effect(EffectType.POISON, 1, multiplicator * stand.current_damage, stand)
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
        target.effects.append(Effect(EffectType.WEAKEN, 1, multiplier, stand))
    return payload, message


def doobie_wah(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 0.4
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    message = f"｢{stand.name}｣ seeks it's enemy!"
    if len(valid_stand) != 0:
        target = random.choice(valid_stand)
        target.effects.append(
            Effect(EffectType.POISON, 1, multiplier * stand.current_damage, stand)
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
        damage += stand.attack(ennemy, multiplier=multiplier)["damage"]
    message = f"｢{stand.name}｣ STOPS TIME! and damages everyone for {int(damage)}"
    return payload, message


def magician_red(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 0.5
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    message = f"｢{stand.name}｣ !"
    if len(valid_stand) != 0:
        target = random.choice(valid_stand)
        target.effects.append(
            Effect(EffectType.POISON, 1, multiplier * stand.current_damage, stand)
        )
    return payload, message


def hierophant_green(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 0.5
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    message = f"No one can deflect the emerald splash!"
    damage = 0
    for s in valid_stand:
        damage += stand.attack(s, multiplier=multiplier)["damage"]
    message = f"Damages everyone for {damage}!"
    return payload, message


def the_fool(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    message = f"｢{stand.name}｣ ! become more resiliant"
    multiplier = 1.1
    stand.ressistance *= multiplier
    return payload, message


def hanged_man(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    message = f"｢{stand.name}｣ find the weak spoT !"
    multiplier = 1.1
    stand.current_critical *= multiplier
    return payload, message


def emperor(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 1.5
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    message = f"｢{stand.name}｣ headshot !"
    if len(valid_stand) != 0:
        target = random.choice(valid_stand)
        damage = stand.attack(target, multiplier=multiplier)["damage"]
        message = f"｢{stand.name}｣ headshot {target.name} for {damage}｣!"
    return payload, message


def justice(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 25
    message = f"｢{stand.name}｣ become more elusive"
    stand.current_speed += multiplier
    return payload, message


def death_13(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier_impared = 5
    multiplier_classic = 0.3
    damage = 0
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    for target in valid_stand:
        if (
            EffectType.STUN in [e.type for e in target.effects]
            or EffectType.SLOW in [e.type for e in target.effects]
            or target.current_speed < target.start_speed
        ):
            damage += stand.attack(target, multiplier=multiplier_impared)["damage"]
        else:
            damage += stand.attack(target, multiplier=multiplier_classic)["damage"]

    message = f"｢{stand.name}｣"
    return payload, message


def high_pristess(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    message = f"｢{stand.name}｣ hardened"
    stand.ressistance *= 1.25
    return payload, message


def geb(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 1.5
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    message = f"｢{stand.name}｣ sneak attack ! !"
    if len(valid_stand) != 0:
        target = random.choice(valid_stand)
        damage = stand.attack(target, multiplier=multiplier)["damage"]
        message = f"｢{stand.name}｣ sneak attack {target.name} for {damage}｣!"
    return payload, message


def horus(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplicator = 2
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    if len(valid_stand) != 0:
        target: "Stand" = random.choice(valid_stand)
        target.effects.append(Effect(EffectType.STUN, multiplicator, 0, stand))
        message = f"｢{stand.name}｣ stuns {target.name} for {multiplicator} rounds!"
    else:
        message = f"｢{stand.name}｣!"
    return payload, message


def atum(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    dice_roll = random.randint(0, 6)
    multiplier = dice_roll
    message = f"｢{stand.name}｣ roll the dices"
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    if len(valid_stand) != 0:
        target: "Stand" = random.choice(valid_stand)
        damage = stand.attack(target, multiplier=multiplier)["damage"]
        message = f"｢{stand.name}｣ roll the dices and land on {dice_roll} ! and damage {target.name} for {damage}"
    return payload, message


def osiris(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    dice_roll = random.randint(0, 6)
    multiplier = dice_roll
    message = f"｢{stand.name}｣ roll the dices"
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    if len(valid_stand) != 0:
        target: "Stand" = random.choice(valid_stand)
        damage = stand.attack(target, multiplier=multiplier)["damage"]
        message = f"｢{stand.name}｣ roll the dices and land on {dice_roll} ! and damage {target.name} for {damage}"
    return payload, message


def red_hot_chili_peper(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 0.01
    dif_damge = (stand.current_hp - stand.start_hp) * multiplier
    stand.current_speed += int(dif_damge)
    message = f"｢{stand.name}｣ gains more speed ! {int(dif_damge)} speed !"
    return payload, message


def echoes_act_2(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 5
    for ennemy in ennemy_stand:
        ennemy.effects.append(Effect(EffectType.SLOW, 3, multiplier, stand))
    message = f"｢{stand.name}｣ slow everyone for {multiplier}!"
    return payload, message


def cinderella(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 5
    for ally in [s for s in allied_stand if s.is_alive()]:
        ally.current_critical += multiplier
    message = f"｢{stand.name}｣ make everyone prettier"
    return payload, message


def highway_star(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 0.5
    message = f"｢{stand.name}｣ schearch nutrient"
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    if len(valid_stand) != 0:
        target: "Stand" = random.choice(valid_stand)
        damage = stand.attack(target, multiplier=multiplier)["damage"]
        stand.current_hp += damage
        message = f"｢{stand.name}｣ damage {target.name} for {damage} and heal himself for {damage}"
    return payload, message


def stray_cat(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    multiplier = 10
    message = f"｢{stand.name}｣ prepares an explosive bubble."
    atck_multiplier = stand.current_critical / multiplier
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    if len(valid_stand) != 0:
        target: "Stand" = random.choice(valid_stand)
        damage = stand.attack(target, multiplier=atck_multiplier)["damage"]
        message = (
            f"｢{stand.name}｣ explode a bubble on {target.name} for {damage} damage"
        )

    return payload, message


def enigma(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    valid_stand = [i for i in ennemy_stand if i.is_alive()]

    message = f"｢{stand.name}｣ schearch their fears."
    if len(valid_stand) != 0:
        target = random.choice(valid_stand)
        if (
            EffectType.STUN in [e.type for e in target.effects]
            or EffectType.SLOW in [e.type for e in target.effects]
            or target.current_speed < target.start_speed
        ):
            target.ressistance *= 0.6
            message = f"｢{stand.name}｣ make {target.name} weak"
    return payload, message


def sex_pistol(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def kraft_work(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def aerosmith(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def man_in_the_miror(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def the_grateful_dead(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def baby_face(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def white_album(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def spice_girl(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


"""
def oasis(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def kiss(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def foo_fighters(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def limp_bizkit(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def diver_down(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def planet_waves(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def green_green_grass_home(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def jail_house_lock(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def sky_high(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def whgitesnake(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def tusk_act_3(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def scary_monster(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def in_a_silent_way(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def tomb_of_boom(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def wired(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def catch_the_rainbow(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def civil_war(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def paisley_park(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def nut_king_call(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def speed_king(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def fun_fun_fun(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def born_this_way(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def i_am_a_rock(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def blue_hawaii(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def ozon_baby(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def doctor_wu(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def space_trucking(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message


def empress(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    # Whatever your code does to the lists above
    # Payload Contain behavior change to the game
    # message is what should be printed to the embed
    return payload, message
"""


def not_implemented(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    payload = get_payload()
    message = f"｢{stand.name}｣ has no power yet"
    payload["is_a_special"] = False
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
    "110": the_world_over_heaven,
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
