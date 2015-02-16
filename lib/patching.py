#
#    Realm667 - An Awesome Awesomeness
#    Copyright (C) 2015 Alexey Lysiuk
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


import random
import re
import string

import doomwad
from iwad_lumps import sprites_doom_all
from iwad_actors import actors_all


# Disable A_SetPitch() calls in DECORATE, suitable for playing without mouselook
no_set_pitch = True

# Disallow class replacement in DECORATE
no_class_replacement = True

# Disallow editor number (doomednum) assignment in DECORATE
no_doomednum = True


# TODO:
# [?] Remove unused lumps like CREDITS or INFO
# [?] Optimize DECORATE lump: remove comments and extra line breaks
# Verbose messages about changes done by patching


def replace_in_lump(name, wad, old, new, optional = False):
    lump = wad.find(name)

    if lump:
        if hasattr(old, 'sub') and hasattr(old, 'groups'):
            # regular expression object
            lump.data = old.sub(new, lump.data, 0)
        else:
            # string object
            lump.data = re.sub(old, new, lump.data, 0, re.IGNORECASE)
    elif not optional:
        print("Error: Cannot find lump {0}".format(name))

def replace_in_decorate(wad, old, new, optional = False):
    replace_in_lump('DECORATE', wad, old, new, optional)

def replace_in_gldefs(wad, old, new, optional = False):
    replace_in_lump('GLDEFS', wad, old, new, optional)


def rename_lump(wad, old, new):
    lump = wad.find(old)

    if lump:
        lump.name = new
    else:
        print("Error: Cannot find lump {0}".format(old))

def remove_lump(wad, name):
    lump = wad.find(name)

    if lump:
        wad.removelump(lump)
    else:
        print("Error: Cannot find lump {0}".format(name))


_sprites = set(sprites_doom_all)

def unique_sprite_name():
    name_chars = string.ascii_uppercase + string.digits
    char_count = len(name_chars)

    while True:
        unique_name = ''

        for i in xrange(0, 4):
            index = random.randint(0, char_count - 1)
            unique_name += name_chars[index]

        if unique_name not in _sprites:
            _sprites.add(unique_name)
            return unique_name

    assert(False)
    return '????'

def rename_sprite(wad, sprite):
    new_name = unique_sprite_name()

    replace_in_decorate(wad,
        r'(\s){0}(\s)'.format(sprite),
        r'\g<1>{0}\g<2>'.format(new_name))
    replace_in_gldefs(wad,
        r'(\s){0}(\s|[\w\s])'.format(sprite),
        r'\g<1>{0}\g<2>'.format(new_name),
        optional = True)

    for lump in wad.spritelumps():
        if lump.name.startswith(sprite):
            lump.name = new_name + lump.name[4:]

def make_unique_sprites(wad):
    """ Find and rename sprites with the same names
        New names are randomly generated """
    for sprite in wad.spritenames():
        if sprite in _sprites:
            rename_sprite(wad, sprite)
        else:
            _sprites.add(sprite)


_actors = set(actors_all)

def rename_actor(decorate, actor):
    suffix = 1

    # generate unique actor name
    while True:
        new_name = '{0}~{1}'.format(actor, suffix)

        if new_name not in _actors:
            _actors.add(new_name)
            break

        suffix += 1

    # replace old name
    replace_pattern = r'(["\s]){0}(["\s])'.format(actor)
    decorate.data = re.sub(replace_pattern,
        r'\g<1>{0}\g<2>'.format(new_name), decorate.data, 0, re.IGNORECASE)

def make_unique_actors(wad):
    """ Find actors in DECORATE and rename them if names are already used """
    decorate = wad.find('DECORATE')
    assert(decorate)

    actor_pattern = r'actor\s+([\w+~.]+)(\s*:\s*[\w+~.]+)?' \
                     '(\s+replace\s+[\w+~.]+)?(\s+\d+)?\s*{'
    actors = re.findall(actor_pattern, decorate.data, re.IGNORECASE)

    for actor in actors:
        if actor[0] in _actors:
            #print('Duplicate actor {0} found!'.format(actor[0]))
            rename_actor(decorate, actor[0])
        else:
            _actors.add(actor[0])


# Asset-specific patches

def apply_patch_10(wad): # Apprentice of D'Sparil
    # fix missing marker
    sprite_end_marker = 'S_END'
    if not wad.find(sprite_end_marker):
        marker = doomwad.Lump(sprite_end_marker, '')
        wad.append(marker)

def apply_patch_225(wad): # Minigun
    # fix sound name collision with #235 Uber Minigun
    replace_in_lump('SNDINFO', wad, r'(\s+)DSMINIGN(\s*)', r'\1DSMNGUNF\2')
    rename_lump(wad, 'DSMINIGN', 'DSMNGUNF')

def apply_patch_228(wad): # Zombieman Rifle
    # fix class name collision with #407 Rifle
    replace_in_decorate(wad,
        r'(actor\s+)Rifle(\s*:\s*\w+)',
        r'\1ZombiemanRifle\2')

def apply_patch_230(wad): # Plasma Gun
    # fix class name collision with #329 Plasma Shotgun
    replace_in_decorate(wad,
        r'([^\w])PlasmaTrail([^\w])',
        r'\1D3PlasmaTrail\2')

def apply_patch_241(wad): # Devastator
    # fix incorrect sprite
    replace_in_decorate(wad, r'(\s)DVST(\s)', r'\1DVGG\2')

def apply_patch_242(wad): # Freeze Rifle
    # fix incorrect sprite
    replace_in_decorate(wad, r'(\s)PLSG(\s)', r'\1FRSG\2')

def apply_patch_266(wad): # Napalm Launcher
    # fix infinite loop in engine caused by wrong state
    replace_in_decorate(wad,
        r'(\s+)GASO(\s+\w\s+)(\d+)(\s+)Loop',
        r'\1GASO\2-1\4stop')

def apply_patch_271(wad): # Saw Thrower
    # fix incorrect sprite
    replace_in_decorate(wad,
        r'Inventory.Icon(\s+)SAWA',
        r'Inventory.Icon\1SAWAA0')

def apply_patch_308(wad): # Doom III Super Shotgun
    # fix sound and sprite name collisions with Doom II Super Shotgun
    replace_in_decorate(wad,
        r'(\w+\s+\w\s+)(\d+\s+)(\w*\s*)A_FireShotgun2',
        '\\g<1>0 \\3A_FireBullets(11.2, 7.1, 20, 5, "BulletPuff")\n'
        '      \\g<1>0 \\3A_PlaySound("doom3ssg/fire", CHAN_WEAPON)\n'
        '      \\g<1>\\2\\3A_GunFlash')
    replace_in_decorate(wad,
        r'(\w+\s+\w\s+\d+\s+\w*\s*)A_OpenShotgun2',
        r'\1A_PlaySound("doom3ssg/open", CHAN_WEAPON)')
    replace_in_decorate(wad,
        r'(\w+\s+\w\s+\d+\s+\w*\s*)A_LoadShotgun2',
        r'\1A_PlaySound("doom3ssg/load", CHAN_WEAPON)')
    replace_in_decorate(wad,
        r'(\w+\s+\w\s+\d+\s+\w*\s*)A_CloseShotgun2',
        r'\1A_PlaySound("doom3ssg/close", CHAN_WEAPON)')
    replace_in_decorate(wad,
        r'Stop(\s+)}(\s+)}',
        'Stop\n   Spawn:\n      SG3W A -1\n      Stop\\1}\\2}')

    rename_lump(wad, 'SGN2A0', 'SG3WA0')
    rename_lump(wad, 'DSDSHTGN', 'SSG3FIRE')
    rename_lump(wad, 'DSDBLOAD', 'SSG3LOAD')
    rename_lump(wad, 'DSDBOPN',  'SSG3OPEN')
    rename_lump(wad, 'DSDBCLS',  'SSG3CLOS')

    sndinfo = doomwad.Lump('SNDINFO',
        'doom3ssg/fire  SSG3FIRE\n'
        'doom3ssg/load  SSG3LOAD\n'
        'doom3ssg/open  SSG3OPEN\n'
        'doom3ssg/close SSG3CLOS\n')
    wad.append(sndinfo)

def apply_patch_314(wad): # Revolver PS
    # fix incorrect sprite
    replace_in_decorate(wad, r'HGUN(\s+)A(\s+)1', r'HGUN\1C\2-1')

def apply_patch_372(wad): # Autogun
    replace_in_gldefs(wad, 'PlickerLight', 'FlickerLight')

def apply_patch_485(wad): # Talisman of the Depths
    # fix class name collision with #482 Rebreather
    replace_in_decorate(wad, r'NoDrown(\s+)', r'NoDrownTalisman\1')

def apply_patch_496(wad): # Nailgun (MG)
    # fix class name collision with #560 Nailgun (SG)
    replace_in_decorate(wad, 'NailBlur', 'NailBlurMG')

def apply_patch_543(wad): # UTNT Pyro-Cannon
    # fix class name collision with #541 Flamethrower
    replace_in_decorate(wad, 'DropFire', 'PyroDropFire')

def apply_patch_560(wad): # Nailgun (SG)
    # fix class name collision with #496 Nailgun (MG)
    replace_in_decorate(wad, 'NailBlur', 'NailBlurSG')

def fix_always_activate(wad):
    # fix incorrect inventory flag
    replace_in_decorate(wad,
        'Inventory.AlwaysActivate',
        'Inventory.AutoActivate')

def apply_patch_577(wad): # Guard Sphere
    fix_always_activate(wad)

def apply_patch_579(wad): # Time Freeze Sphere
    fix_always_activate(wad)

def remove_credit_lump(wad):
    # remove unused text lump conflicting with Doom IWADs
    remove_lump(wad, 'CREDIT')

def apply_patch_582(wad): # Super Crossbow
    remove_credit_lump(wad)
    # fix missing marker
    sprite_end_marker = 'SS_END'
    if not wad.find(sprite_end_marker):
        marker = doomwad.Lump(sprite_end_marker, '')
        wad.append(marker)

def apply_patch_608(wad): # Armor Shard
    remove_credit_lump(wad)

def apply_patch_659(wad): # Pulse Rifle UAC
    # fix class name collision with #522 Pulse Rifle
    replace_in_decorate(wad,
        r'(actor\s+)PulseRifle(\s*:\s*\w+)',
        r'\1PulseRifleUAC\2')

def apply_patch_671(wad): # Food Barrel
    # fix class name collisions with embedded actors
    replace_in_decorate(wad, 'Meat1', 'MeatBeef')
    replace_in_decorate(wad, 'Meat2', 'MeatCheese')
    replace_in_decorate(wad, 'Meat3', 'MeatFish')

def apply_patch_685(wad): # Ammo Satchels
    # fix class name collision with ammo from Strife
    replace_in_decorate(wad, 'AmmoSatchel', 'AmmoSatchelR667')

def apply_patch_762(wad): # Model 1887
    # fix wrong end marker
    rename_lump(wad, 'SS_STOP', 'SS_END')

def apply_patch_795(wad): # Missile Pod
    # fix usage of missing actor class
    replace_in_decorate(wad,
        r'(\w+\s+\w\s+\d\s+A_SpawnItemEx\s*\(\s*"MissileFlameTrail")', r'//\1')

def apply_patch_804(wad): # Light Machinegun
    # fix class name collision with #233 Machinegun
    replace_in_decorate(wad,
        r'(actor\s+)Machinegun(\s*:\s*\w+)',
        r'\1LightMachinegun\2')

def apply_patch_817(wad): # Arbalest of the Ancients
    # fix class name collision with #582 Super Crossbow
    replace_in_decorate(wad,
        r'([^\w])SuperCrossbow',
        r'\1Arbalest')


broken_keyconfs = (
    226, # Sawed Off
    235, # Uber Minigun
    240, # Seeker Bazooka
    241, # Devastator
    246, # EgoSmasher
    252, # Tesla Cannon
    257, # Power Nailgun
    263, # Hunter Shotgun
    266, # Napalm Launcher
    267, # Necrovision MG40
    269, # Pulse Machinegun
    273, # Swat Shotgun
    274, # Western Shotgun
    283, # TommyGun
    308, # Doom 2.5 SSG
    314, # Revolver PS
    328, # Spellbinder
    329, # Plasma Shotgun
    330, # Butchergun Chaingun
    509, # Prox Launcher
    510, # Vile Staff
    521, # Mag .60
    536, # Jackbomb
    626, # D'sparil Staff
)

# list of weapons with A_SetPitch() call(s) in DECORATE
# These weapons change player's pitch preventing smooth playing
# without mouselook and so they are in the following list
# Some weapons modify player's pitch but then restore it back
# These weapons are commented out in the following list

weapons_change_pitch = (
    432, # Autogun
#    0445, # Coachgun
#    0513, # Smasher
    559, # Glock 18
    585, # AA12 Shotgun
#    599, # MP40
    600, # M40A1 Sniper Rifle
    684, # MP5
    686, # G3
    719, # Hunting Rifle
)


re_no_set_pitch = re.compile(r'\s+A_SetPitch\s*\([\+\w\s\.\+\-\*\\]+\)', re.IGNORECASE)
re_no_class_replacement = re.compile(r'(actor\s+[\w~.]+\s*:\s*[\w~.]+)\s+replaces\s+[\w~.]+', re.IGNORECASE)
re_no_doomednum = re.compile(r'(actor\s+[\w~.]+(\s*:\s*[\w~.]+)?\s+(replaces\s+[\w~.]+)?)\s*\d*', re.IGNORECASE)


def apply_patch(id, wad):
    # Fix weapon slot and player class resetting
    if id in broken_keyconfs:
        remove_lump(wad, 'KEYCONF')

    func_name = 'apply_patch_{0}'.format(id)

    if func_name in globals():
        globals()[func_name](wad)

    if no_set_pitch and id in weapons_change_pitch:
        replace_in_decorate(wad, re_no_set_pitch, '')
    if no_class_replacement:
        replace_in_decorate(wad, re_no_class_replacement, r'\1')
    if no_doomednum:
        replace_in_decorate(wad, re_no_doomednum, r'\1')

    make_unique_sprites(wad)

"""
    Unique actors name patch have at least two issues:
    1) Actor name and reserved word (property, flag, etc) can be the same
       Without complete DECORATE parsing it's impossible to distinguish
       these cases, regular expression in not enough...
    2) Actors referenced in menu can be renamed
       It's quite problematic to generate menu automatically,
       or even to update it according to changes in DECORATE
    3) Renaming of ammo actors will produce a new ammo type
       Although it's incorrect as the same ammo can be used by several weapons
    That's why this patch is disabled
"""
##    make_unique_actors(wad)
