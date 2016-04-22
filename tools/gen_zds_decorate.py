#!/usr/bin/env python

#
#    Realm667 - An Awesome Awesomeness
#    Copyright (C) 2015, 2016 Alexey Lysiuk
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys

# all modules are in the lib directory
sys.path[0] = os.path.dirname(os.path.abspath(__file__)) + '/../lib'

import utils


# ==============================================================================


_MONSTERS = (
    #  Class name    | Reward  | Has XDeath
    ('ZombieMan',          10,     True),
    ('ShotgunGuy',         25,     True),
    ('ChaingunGuy',        50,     True),
    ('WolfensteinSS',      40,     True),
    ('DoomImp',            25,     True),
    ('Demon',              50,    False),
    ('Spectre',            70,    False),
    ('Cacodemon',         150,    False),
    ('BaronOfHell',       500,    False),
    ('HellKnight',        250,    False),
    ('PainElemental',     300,    False),
    ('Revenant',          250,    False),
    ('Arachnotron',       300,    False),
    ('Fatso',             300,    False),
    ('Archvile',          500,    False),
    ('SpiderMastermind', 1000,    False),
    ('Cyberdemon',       2000,    False),
    ('BossBrain',        1000,    False),
    # nothing for LostSoul and CommanderKeen :)
    # TODO: Stealth monsters ?
)

_MONSTER_PATTERN = '''
actor ZDS{0} : {0} replaces {0}
{{
    DropItem None

    states
    {{
{1}    }}
}}
'''

_MONSTER_STATE_PATTERN = '''    {0}:
        TNT1 A 0 A_GiveInventory("ZDSSoul", {1}, AAPTR_PLAYER1)
        goto Super::{0}
'''


def _generate_monsters():
    result = []

    for monster in _MONSTERS:
        class_name = monster[0]
        reward = monster[1]
        has_xdeath = monster[2]

        states = _MONSTER_STATE_PATTERN.format('Death', reward)

        if has_xdeath:
            states += _MONSTER_STATE_PATTERN.format('XDeath', reward)

        definition = _MONSTER_PATTERN.format(class_name, states)
        result.append(definition)

    return result


# ==============================================================================


_PICKUPS = (
    #  Class name            | Price    | Amount
    # -----------------------+----------+--------
    #  Weapons               |          |
    ('Chainsaw',                 100,        1),
    ('Shotgun',                  100,        1),
    ('SuperShotgun',             200,        1),
    ('Chaingun',                 150,        1),
    ('RocketLauncher',           300,        1),
    ('PlasmaRifle',              300,        1),
    ('BFG9000',                  500,        1),
    #  Ammo                  |          |
    ('Clip',                       5,       10),
    ('ClipBox',                   25,       50),
    ('Shell',                     20,        4),
    ('ShellBox',                 100,       20),
    ('RocketAmmo',                10,        1),
    ('RocketBox',                 50,        5),
    ('Cell',                      20,       20),
    ('CellPack',                 100,      100),
    ('Backpack',                 200,        1),
    # Health                 |          |
    ('HealthBonus',                1,        1),
    ('Stimpack',                  10,        1),
    ('Medikit',                   25,       25),
    # Armor                  |          |
    ('ArmorBonus',                 1,        1),
    ('GreenArmor',               100,        1),
    ('BlueArmor',                200,        1),
    # Artifacts              |          |
    ('InvulnerabilitySphere',    500,        1),
    ('Soulsphere',               200,        1),
    ('Megasphere',               400,        1),
    ('BlurSphere',               200,        1),
    ('RadSuit',                  100,        1),
    ('Infrared',                 100,        1),
    ('Allmap',                   500,        1),
    ('Berserk',                  250,        1),
)

_PICKUP_PATTERN = '''
actor ZDS{0} : CustomInventory replaces {0}
{{
    Inventory.PickupMessage "You picked up {1} souls"

    States
    {{
    Spawn:
        ZDSS ABCB 6 BRIGHT
        loop
    Pickup:
        TNT1 A 0 A_GiveInventory("ZDSSoul", {1})
        stop
    }}
}}
'''


def _generate_pickups():
    result = []

    for item in _PICKUPS:
        class_name = item[0]
        price = item[1]

        definition = _PICKUP_PATTERN.format(class_name, price)
        result.append(definition)

    return result


# ==============================================================================


def _write_file(path, lines):
    output_file = open(utils.data_project_path() + path, 'w')
    output_file.writelines(utils.license_header('//'))
    output_file.writelines(lines)
    output_file.close()


utils.set_mode(utils.MODE_ZDS)

_write_file('actors/doom/monsters.txt', _generate_monsters())
_write_file('actors/doom/pickups.txt', _generate_pickups())
