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
import subprocess
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
    #  Class name             | Visible name                 | Price    | Amount
    # ------------------------+------------------------------+----------+--------
    ('Weapons',),
    ('Chainsaw',                'Chainsaw',                      100,        1),
    ('Shotgun',                 'Shotgun',                       100,        1),
    ('SuperShotgun',            'Super Shotgun',                 200,        1),
    ('Chaingun',                'Chaingun',                      150,        1),
    ('RocketLauncher',          'Rocket Launcher',               300,        1),
    ('PlasmaRifle',             'Plasma Gun',                    300,        1),
    ('BFG9000',                 'BFG9000',                       500,        1),

    ('Ammo',),
    ('Clip',                    'Clip of Bullets',                 5,       10),
    ('ClipBox',                 'Box of Bullets',                 25,       50),
    ('Shell',                   'Shotgun Shells',                 20,        4),
    ('ShellBox',                'Box of Shotgun Shells',         100,       20),
    ('RocketAmmo',              'Rocket',                         10,        1),
    ('RocketBox',               'Box of Rockets',                 50,        5),
    ('Cell',                    'Energy Cell',                    20,       20),
    ('CellPack',                'Energy Cell Pack',              100,      100),
    ('Backpack',                'Backpack',                      200,        1),

    ('Health',),
    ('HealthBonus',             'Health Bonus',                    1,        1),
    ('Stimpack',                'Stimpack',                       10,        1),
    ('Medikit',                 'Medikit',                        25,       25),

    ('Armor',),
    ('ArmorBonus',              'Armor Bonus',                     1,        1),
    ('GreenArmor',              'Armor',                         100,        1),
    ('BlueArmor',               'MegaArmor',                     200,        1),

    ('Artifacts',),
    ('InvulnerabilitySphere',   'Invulnerability',               500,        1),
    ('Soulsphere',              'Supercharge',                   200,        1),
    ('Megasphere',              'MegaSphere',                    400,        1),
    ('BlurSphere',              'Partial Invisibility',          200,        1),
    ('RadSuit',                 'Radiation Shielding Suit',      100,        1),
    ('Infrared',                'Light Amplification Visor',     100,        1),
    ('Allmap',                  'Computer Area Map',             500,        1),
    ('Berserk',                 'Berserk',                       250,        1),
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
        if 1 == len(item):
            # Skip category
            continue

        class_name = item[0]
        price = item[2]

        definition = _PICKUP_PATTERN.format(class_name, price)
        result.append(definition)

    return result


# ==============================================================================


_MENUDEF_PATTERN = '''
OptionMenu "Menu_R667ZDS"
{{
    StaticText "Realm667 - ZDoomed Souls", 1
{0}}}
'''

_MENUDEF_CATEGORY_PATTERN = '    StaticText ""\n\n    StaticText "Buy {0}"\n'
_MENUDEF_ITEM_PATTERN = '    Command "{0}", "r667zds {1}"\n'


def _generate_menudef():
    menu = ''

    for item in _PICKUPS:
        if 1 == len(item):
            # Category
            menu += _MENUDEF_CATEGORY_PATTERN.format(item[0])
        else:
            # Item to
            class_name = item[0]
            visible_name = item[1]

            menu += _MENUDEF_ITEM_PATTERN.format(visible_name, class_name)

    return _MENUDEF_PATTERN.format(menu)


# ==============================================================================


_ACS_INCLUDE_PATTERN = '''
#define CLASS_COUNT {0}

str CLASS_NAMES[CLASS_COUNT] =
{{{1}
}};

int PRICES[CLASS_COUNT] =
{{{2}
}};

int AMOUNTS[CLASS_COUNT] =
{{{3}
}};
'''


def _generate_acs_include():
    class_names = ''
    prices = ''
    amounts = ''

    for item in _PICKUPS:
        if 1 == len(item):
            # Skip category
            continue

        class_name = item[0]
        class_names += '\n    "{}",'.format(class_name)

        price = item[2]
        prices += '\n    {},'.format(price)

        amount = item[3]
        amounts += '\n    {},'.format(amount)

    return _ACS_INCLUDE_PATTERN.format(len(_PICKUPS), class_names, prices, amounts)


# ==============================================================================


def _compile_acs():
    data_path = utils.data_project_path()
    input_path = data_path + 'scripts/r667zds.acs'
    output_path = data_path + 'acs/r667zds.o'

    args = (utils.exe_path('acc'), input_path, output_path)

    proc = subprocess.Popen(args)
    proc.communicate()


# ==============================================================================


def _write_file(path, lines):
    output_file = open(utils.data_project_path() + path, 'w')
    output_file.writelines(utils.license_header('//'))
    output_file.writelines(lines)
    output_file.close()


utils.set_mode(utils.MODE_ZDS)

_write_file('actors/doom/monsters.txt', _generate_monsters())
_write_file('actors/doom/pickups.txt', _generate_pickups())
_write_file('menudef.txt', _generate_menudef())
_write_file('scripts/r667zds.h', _generate_acs_include())

_compile_acs()
