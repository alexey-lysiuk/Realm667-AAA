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
    ('ZombieMan', 10),
    ('ShotgunGuy', 20),
    # ...
)

_MONSTER_PATTERN = '''
actor ZDS{0} : {0} replaces {0}
{{
    DropItem None

    states
    {{
    Death:
        TNT1 A 0 A_GiveInventory("ZDSSoul", {1}, AAPTR_PLAYER1)
        goto Super::Death
    XDeath:
        TNT1 A 0 A_GiveInventory("ZDSSoul", {1}, AAPTR_PLAYER1)
        goto Super::XDeath
    }}
}}
'''


# ==============================================================================


_PICKUPS = (
    # Ammo
    ('Clip', 5),
    ('ClipBox', 20),
    # Health
    ('HealthBonus', 5),
    ('Stimpack', 10),
    ('Medikit', 20),
    # ...
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


# ==============================================================================


utils.set_mode(utils.MODE_ZDS)


def _generate_decorate(content, pattern):
    result = []

    for item in content:
        definition = pattern.format(item[0], item[1])
        result.append(definition)

    return result


def _write_file(path, lines):
    output_file = open(utils.data_project_path() + path, 'w')
    output_file.writelines(utils.license_header('//'))
    output_file.writelines(lines)
    output_file.close()


_monsters_decorate = _generate_decorate(_MONSTERS, _MONSTER_PATTERN)
_write_file('actors/doom/monsters.txt', _monsters_decorate)

_pickups_decorate = _generate_decorate(_PICKUPS, _PICKUP_PATTERN)
_write_file('actors/doom/pickups.txt', _pickups_decorate)
