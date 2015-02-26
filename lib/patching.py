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
from iwad_lumps import sprites_all
from iwad_sndinfo import logical_sounds_all, sounds_lumps_all
from case_insensitive import CaseInsensitiveSet


# Allow A_SetPitch() calls in DECORATE,
# suitable for playing with mouselook enabled
allow_set_pitch = False

# Allow class replacement in DECORATE
allow_class_replacement = False

# Allow editor number (doomednum) assignment in DECORATE
allow_doomednum = False


# ==============================================================================


VERBOSITY_NONE = 0
VERBOSITY_LOW  = 1
VERBOSITY_HIGH = 2


verbosity_level = VERBOSITY_NONE


def _verbose_print(level, message):
    if verbosity_level >= level:
        print(' * {0}'.format(message))


# ==============================================================================


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

def replace_in_decorate(wad, old, new):
    replace_in_lump('DECORATE', wad, old, new)

def replace_in_gldefs(wad, old, new):
    for alias in ('GLDEFS', 'DOOMDEFS', 'HTICDEFS', 'HEXNDEFS', 'STRFDEFS'):
        replace_in_lump(alias, wad, old, new, optional = True)

def replace_in_sndinfo(wad, old, new):
    replace_in_lump('SNDINFO', wad, old, new)


def rename_lump(wad, old, new):
    lump = wad.find(old)

    if lump:
        lump.name = new

        _verbose_print(VERBOSITY_LOW,
            'Lump {0} was renamed to {1}'.format(old, new))
    else:
        print('Error: Cannot find lump {0}'.format(old))

def add_lump(wad, name, content):
    lump = wad.find(name)

    if lump:
        print('Error: Lump {0} is already exist'.format(name))
    else:
        lump = doomwad.Lump(name, content)
        wad.append(lump)

        _verbose_print(VERBOSITY_LOW,
            'Lump {0} was added'.format(name))

def remove_lump(wad, name):
    lump = wad.find(name)

    if lump:
        wad.removelump(lump)

        _verbose_print(VERBOSITY_LOW,
            'Lump {0} was deleted'.format(name))
    else:
        print("Error: Cannot find lump {0}".format(name))


def remove_unused_sound(wad, lump_name):
    sndinfo = wad.find('SNDINFO')
    if sndinfo:
        if lump_name not in sndinfo.data:
            remove_lump(wad, lump_name)


# ==============================================================================


# the following dictionary in the same format as returned from WadFile.spritemapping()
# single incorrect frame is added for all sprites,
# so sprites from IWADs will always be different and
# any possibility of name collision is avoided
_sprites = { sprite: { None: None } for sprite in sprites_all }

def _generate_unique_sprite_name(sprite, frames):
    name_chars = string.ascii_uppercase + string.digits
    char_count = len(name_chars)

    name_length = len(sprite)

    while True:
        unique_name = ''

        for i in xrange(0, name_length):
            index = random.randint(0, char_count - 1)
            unique_name += name_chars[index]

        if unique_name not in _sprites:
            _sprites[unique_name] = frames
            return unique_name

    assert(False)
    return None

_sprites_renames = { }

def _generate_new_sprite_name(sprite, frames):
    new_name = None

    if sprite in _sprites_renames:
        renames = _sprites_renames[sprite]

        for rename in renames:
            if _sprites[rename] == frames:
                new_name = rename
                break

    if not new_name:
        new_name = _generate_unique_sprite_name(sprite, frames)

    return new_name

def rename_sprite(wad, old, new):
    search_pattern = r'([\s"])%s(\w{0,4}[\s"])' % old
    replace_pattern = r'\g<1>{0}\g<2>'.format(new)

    replace_in_decorate(wad,
        r'([\s"])%s([\s"]|\w{2}[\s"])' % old, replace_pattern)
    replace_in_lump('ANIMDEFS', wad,
        search_pattern, replace_pattern, optional = True)
    replace_in_lump('DECALDEF', wad,
        search_pattern, replace_pattern, optional = True)
    replace_in_gldefs(wad,
        search_pattern, replace_pattern)

    for lump in wad.spritelumps():
        if lump.name.startswith(old):
            lump.name = new + lump.name[4:]

    if old in _sprites_renames:
        _sprites_renames[old].append(new)
    else:
        _sprites_renames[old] = [new]

    _verbose_print(VERBOSITY_LOW,
        'Sprite {0} was renamed to {1}'.format(old, new))

def make_unique_sprites(wad):
    """ Find and rename sprites with the same name but different content
        New names are randomly generated """
    for name, frames in wad.spritemapping().iteritems():
        if name in _sprites:
            if frames != _sprites[name]:
                new_name = _generate_new_sprite_name(name, frames)
                rename_sprite(wad, name, new_name)
        else:
            _sprites[name] = frames


# ==============================================================================


_actors = CaseInsensitiveSet()

def rename_actor(wad, actor):
    suffix = 1

    # generate unique actor name
    while True:
        new_name = '{0}_{1}'.format(actor, suffix)

        if new_name not in _actors:
            _actors.add(new_name)
            break

        suffix += 1

    # replace old name
    old_pattern = r'(["\s]){0}(["\s])'.format(actor)
    new_pattern = r'\g<1>{0}\g<2>'.format(new_name)

    replace_in_decorate(wad, old_pattern, new_pattern)
    replace_in_gldefs(wad, old_pattern, new_pattern)

    _verbose_print(VERBOSITY_LOW,
        'Actor class {0} was renamed to {1}'.format(actor, new_name))


# TODO: is it ever possible to do this using ONE regex?
actor_stateful_pattern  = r'actor\s+%s[\s:{].*?(states\s*{.+?}).*?}\s*'
actor_stateless_pattern = r'actor\s+%s[\s:{].*?}\s*'

def remove_actor(decorate, name):
    for pattern in (actor_stateful_pattern, actor_stateless_pattern):
        decorate.data = re.sub(pattern % name, '',
            decorate.data, 0, re.IGNORECASE | re.DOTALL)

    _verbose_print(VERBOSITY_LOW,
        'Actor class {0} was deleted'.format(name))

actor_header_regex = re.compile(r'(\s|^)actor\s+([\w+~.]+).*?{',
    re.IGNORECASE | re.DOTALL)

_duplicate_actors = CaseInsensitiveSet((
    # ammo, mandatory to remove
    'Nails',
    'Darkmana',
    'Gas',
    'BigGas',
    # other actors
    'NapalmDebris',
    'PlasmaBolterShot1',
    'PlasmaBolterShot1Trail',
    # TODO: extend with other identical actors
),)

def make_unique_actors(wad):
    decorate = wad.find('DECORATE')
    assert(decorate)

    # comments needs to be removed from DECORATE,
    # as actor renaming and removal may fail otherwise
    # consider two actors in the same lump, but one is commented out
    # for instance, see #272 Sniper Rifle
    # actually, there is an other way to do this without comment removal
    # but this will increase complexity even more
    doomwad.striplumpcomments(decorate)

    for dummy, actor in actor_header_regex.findall(decorate.data):
        if actor in _actors:
            if actor in _duplicate_actors:
                remove_actor(decorate, actor)
            else:
                rename_actor(wad, actor)
        else:
            _actors.add(actor)


# ==============================================================================


_lumps = { }

_included_names = {
    'ANIMDEFS',
    'DECALDEF',
    'DECORATE',
    'GLDEFS',
    'KEYCONF',
    'SNDINFO',
    'TEXTURES',
}

_excluded_names = {
    'CREDIT',   # informational, but fixes conflict with texture from IWADs
    'CREDITS',  # informational
    'INFO',     # informational
    'UPDATES',  # informational
    'RELOADIN', # alternative DECORATE lumps
    '--------',
}

def is_lump_needed(lump):
    name = lump.name

    if name in _excluded_names:
        _verbose_print(VERBOSITY_HIGH,
            'Unwanted lump {0} was deleted'.format(name))
        return False

    if lump.marker or name in _included_names:
        return True

    hash = lump.hash()

    if name in _lumps:
        if hash in _lumps[name]:
            _verbose_print(VERBOSITY_HIGH,
                'Duplicate lump {0} was deleted'.format(name))
            return False
        else:
            _lumps[name].add(hash)
            return True
    else:
        _lumps[name] = { hash }
        return True

def optimize(wad):
    wad.filter(is_lump_needed)


# ==============================================================================


def _generate_unique_lump_name():
    name_chars = string.ascii_uppercase + string.digits + '_'
    char_count = len(name_chars)

    while True:
        unique_name = ''

        for i in xrange(0, 8):
            index = random.randint(0, char_count - 1)
            unique_name += name_chars[index]

        if unique_name not in _lumps:
            return unique_name

    assert(False)
    return None


# ==============================================================================


# map sound lump names to a hash of lump's content
_sound_lumps = { name: None for name in sounds_lumps_all }

# map old names to a set of new names
_sound_lump_renames = { }

def rename_sound_lump(wad, name, content_hash):
    """ Rename sound lump in WAD file and change references to it in SNDINFO """
    new_name = None

    if name in _sound_lump_renames:
        for rename in _sound_lump_renames[name]:
            if rename in _sound_lumps and _sound_lumps[rename] == content_hash:
                new_name = rename
                break
    else:
        _sound_lump_renames[name] = set()

    if not new_name:
        new_name = _generate_unique_lump_name()
        _sound_lump_renames[name].add(new_name)
        _sound_lumps[new_name] = content_hash

    rename_lump(wad, name, new_name)
    replace_in_sndinfo(wad,
        r'(\s){0}(\s|$)'.format(name),
        r'\g<1>{0}\g<2>'.format(new_name))

rename_sound_lump.mapping_type = doomwad.SoundMapping.LUMP_TO_CONTENT
rename_sound_lump.global_mapping = _sound_lumps


# map logical sound name to a lump name, based on SNDINFO lump content
_logical_sounds = { name: None for name in logical_sounds_all }

def rename_logical_sound(wad, logical_name, lump_name):
    """ Rename logical sound in SNDINFO lump and change references to it in DECORATE """
    new_name = 'r667aaa/' + _generate_unique_lump_name().lower()
    _logical_sounds[new_name] = lump_name

    replace_in_decorate(wad,
        '"{0}"'.format(logical_name),
        '"{0}"'.format(new_name))
    replace_in_sndinfo(wad,
        r'(^|\s){0}(\s)'.format(logical_name),
        r'\g<1>{0}\g<2>'.format(new_name))

    _verbose_print(VERBOSITY_LOW,
        'Logical sound {0} was renamed to {1}'.format(logical_name, new_name))

    return new_name

rename_logical_sound.mapping_type = doomwad.SoundMapping.LOGICAL_TO_LUMP
rename_logical_sound.global_mapping = _logical_sounds


def _make_unique_sounds_with_mapping(wad, rename_func):
    mapping = wad.soundmapping(rename_func.mapping_type)

    for key in mapping:
        value = mapping[key]

        if value and key in rename_func.global_mapping:
            if value != rename_func.global_mapping[key]:
                rename_func(wad, key, value)
        else:
            rename_func.global_mapping[key] = value

def make_unique_sounds(wad):
    _make_unique_sounds_with_mapping(wad, rename_sound_lump)
    _make_unique_sounds_with_mapping(wad, rename_logical_sound)


# ==============================================================================

# Asset-specific patches

def _apply_patch_10(wad): # Apprentice of D'Sparil
    # fix missing marker
    sprite_end_marker = 'S_END'
    if not wad.find(sprite_end_marker):
        marker = doomwad.Lump(sprite_end_marker, '')
        wad.append(marker)

def _apply_patch_14(wad): # Bat
    # remove sprites with broken transparency
    # lumps from #185 Baphomet's Eyes will be used
    # they are the same sprites but with correct alpha channel
    wad.removesprite('BFAM')

def _apply_patch_33(wad): # Darkness Rift
    # fix wrong class name
    replace_in_decorate(wad, '"Fatty"', '"Fatso"')

def add_dummy_brighmap(wad, name):
    # fix 'brightmap not found' warning in console
    brightmap = doomwad.Lump(name,
        # 16x16 pixels image filled with black in PNG format
        '\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52'
        '\x00\x00\x00\x10\x00\x00\x00\x10\x08\x04\x00\x00\x00\xb5\xfa\x37'
        '\xea\x00\x00\x00\x15\x49\x44\x41\x54\x28\xcf\x63\x64\xf8\xcf\x80'
        '\x17\x30\x31\x30\x8c\x2a\x18\x39\x0a\x00\x2f\x20\x01\x1f\x24\xfd'
        '\x05\xb8\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82')
    wad.append(brightmap)

def _apply_patch_40(wad): # Double Chaingunner
    add_dummy_brighmap(wad, 'BMDPOSE5')

def _apply_patch_44(wad): # Fallen
    add_dummy_brighmap(wad, 'BMFALNM0')

def _apply_patch_52(wad): # Hell Apprentice
    remove_unused_sound(wad, 'DSDASH')

def _apply_patch_55(wad): # Hell Smith
    remove_unused_sound(wad, 'DSDASH')

def fix_actor_borgnail2(wad):
    # fix wrong class name
    replace_in_decorate(wad, '"BornNail2"', '"BorgNail2"')

def _apply_patch_66(wad): # Nail Borg
    fix_actor_borgnail2(wad)

def _apply_patch_70(wad): # Nightmare Demon
    # fix brightmap collisions with #17 Blood Fiend
    for lump in wad:
        if lump.name.startswith('BMSAR2'):
            lump.name = 'BMNMDM' + lump.name[6:]
    replace_in_gldefs(wad, r'(\s)BMSAR2(\w{2}\s)', r'\1BMNMDM\2')

def _apply_patch_71(wad): # Plasma Demon
    # remove sounds conflicting with Doom IWADs
    remove_unused_sound(wad, 'DSFIRSHT')
    remove_unused_sound(wad, 'DSFIRXPL')

def _apply_patch_151(wad): # Phantom
    # fix wrong class name
    replace_in_decorate(wad, '"GhostHatch"', '"PhantomHatch"')

def _apply_patch_191(wad): # Hangman
    # remove unused demo map
    wad.filter(lambda lump: 'MAP999' != lump.name       \
                        and 'MAP999' != lump.namespace)

def _apply_patch_228(wad): # Zombieman Rifle
    # fix class name collision with #407 Rifle
    replace_in_decorate(wad,
        r'(actor\s+)Rifle(\s*:\s*\w+)',
        r'\1ZombiemanRifle\2')

def _apply_patch_241(wad): # Devastator
    # fix incorrect sprite
    replace_in_decorate(wad, r'(\s)DVST(\s)', r'\1DVGG\2')

def _apply_patch_242(wad): # Freeze Rifle
    # fix incorrect sprite
    replace_in_decorate(wad, r'(\s)PLSG(\s)', r'\1FRSG\2')

def _apply_patch_266(wad): # Napalm Launcher
    # fix infinite loop in engine caused by wrong state
    replace_in_decorate(wad,
        r'(\s+)GASO(\s+\w\s+)(\d+)(\s+)Loop',
        r'\1GASO\2-1\4stop')

def _apply_patch_271(wad): # Saw Thrower
    # fix incorrect sprite
    replace_in_decorate(wad,
        r'Inventory.Icon(\s+)SAWA',
        r'Inventory.Icon\1SAWAA0')

def _apply_patch_284(wad): # Arachnobaron
    add_dummy_brighmap(wad, 'BMARBRB5')

def _apply_patch_308(wad): # Doom III Super Shotgun
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

    rename_lump(wad, 'SGN2A0',   'SG3WA0'  )
    rename_lump(wad, 'DSDSHTGN', 'SSG3FIRE')
    rename_lump(wad, 'DSDBLOAD', 'SSG3LOAD')
    rename_lump(wad, 'DSDBOPN',  'SSG3OPEN')
    rename_lump(wad, 'DSDBCLS',  'SSG3CLOS')

    add_lump(wad, 'SNDINFO',
        'doom3ssg/fire  SSG3FIRE\n'
        'doom3ssg/load  SSG3LOAD\n'
        'doom3ssg/open  SSG3OPEN\n'
        'doom3ssg/close SSG3CLOS\n')

def _apply_patch_314(wad): # Revolver PS
    # fix incorrect sprite
    replace_in_decorate(wad, r'HGUN(\s+)A(\s+)1', r'HGUN\1C\2-1')

def _apply_patch_316(wad): # Agaures
    add_dummy_brighmap(wad, 'BMAGURG5')

def _apply_patch_318(wad): # Moloch
    # fix usage of missing actor class
    replace_in_decorate(wad,
        r'(\w+\s+\w\s+\d\s+A_CustomMissile\s*\(\s*"MolochDeathFire")', r'//\1')

def _apply_patch_337(wad): # Nail Borg Commando
    fix_actor_borgnail2(wad)

def _apply_patch_372(wad): # Autogun
    # fix error in keyword
    replace_in_gldefs(wad, 'PlickerLight', 'FlickerLight')

def _apply_patch_412(wad): # Power Stimpack
    # fix wrong class name
    replace_in_gldefs(wad, r'(\s)PowerStimpack(\s)', r'\1PowerStim\2')

def _apply_patch_433(wad): # Chiller
    # fix missing class name
    replace_in_decorate(wad, '"ChillerFog2"', '"ChillerFog"')

def _apply_patch_485(wad): # Talisman of the Depths
    # fix class name collision with #482 Rebreather
    # cannot be resolved automatically because of optional Power... prefix
    replace_in_decorate(wad, r'NoDrown(\s+)', r'NoDrownTalisman\1')

def _apply_patch_511(wad): # Lightbringer'
    # fix wrong class and light names
    replace_in_gldefs(wad, r'(\s)SunProjectile1(\s)', r'\1SunProjectile\2')

def _apply_patch_536(wad): # Jackbomb
    # fix missing class reference
    regex = re.compile(r'object\s+Curse\s+{.*?\s+}\s+}\s*', re.IGNORECASE | re.DOTALL)
    replace_in_gldefs(wad, regex, '')

def fix_always_activate(wad):
    # fix incorrect inventory flag
    replace_in_decorate(wad,
        'Inventory.AlwaysActivate',
        'Inventory.AutoActivate')

def _apply_patch_577(wad): # Guard Sphere
    fix_always_activate(wad)

def _apply_patch_579(wad): # Time Freeze Sphere
    fix_always_activate(wad)

def _apply_patch_582(wad): # Super Crossbow
    # fix missing marker
    sprite_end_marker = 'SS_END'
    if not wad.find(sprite_end_marker):
        marker = doomwad.Lump(sprite_end_marker, '')
        wad.append(marker)

def _apply_patch_604(wad): # Dark Inquisitor
    # fix lump name conflict with Doom IWADs
    rename_sound_lump(wad, 'STEP2', None)

def _apply_patch_620(wad): # Chesire Cacodemon
    # fix wrong class names
    replace_in_gldefs(wad, r'(\s)CheshBall(\s)', r'\1ChesBallA\2')

def _apply_patch_659(wad): # Pulse Rifle UAC
    # fix class name collision with #522 Pulse Rifle
    replace_in_decorate(wad,
        r'(actor\s+)PulseRifle(\s*:\s*\w+)',
        r'\1PulseRifleUAC\2')

def _apply_patch_671(wad): # Food Barrel
    # fix class name collisions with embedded actors
    replace_in_decorate(wad, 'Meat1', 'MeatBeef')
    replace_in_decorate(wad, 'Meat2', 'MeatCheese')
    replace_in_decorate(wad, 'Meat3', 'MeatFish')

def _apply_patch_685(wad): # Ammo Satchels
    # fix class name collision with ammo from Strife
    replace_in_decorate(wad, 'AmmoSatchel', 'AmmoSatchelR667')

def _apply_patch_762(wad): # Model 1887
    # fix wrong end marker
    rename_lump(wad, 'SS_STOP', 'SS_END')

def _apply_patch_795(wad): # Missile Pod
    # fix usage of missing actor class
    replace_in_decorate(wad,
        r'(\w+\s+\w\s+\d\s+A_SpawnItemEx\s*\(\s*"MissileFlameTrail")', r'//\1')

def _apply_patch_804(wad): # Light Machinegun
    # fix class name collision with #233 Machinegun
    replace_in_decorate(wad,
        r'(actor\s+)Machinegun(\s*:\s*\w+)',
        r'\1LightMachinegun\2')

def _apply_patch_817(wad): # Arbalest of the Ancients
    # fix class name collision with #582 Super Crossbow
    replace_in_decorate(wad,
        r'([^\w])SuperCrossbow',
        r'\1Arbalest')


# ==============================================================================


_broken_keyconfs = (
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
    465, # Salvation Sphere
    509, # Prox Launcher
    510, # Vile Staff
    521, # Mag .60
    536, # Jackbomb
    539, # Blood Lich
    552, # Hierophant
    626, # D'sparil Staff
)

# list of weapons with A_SetPitch() call(s) in DECORATE
# These weapons change player's pitch preventing smooth playing
# without mouselook and so they are in the following list
# Some weapons modify player's pitch but then restore it back
# These weapons are commented out in the following list

_weapons_change_pitch = (
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


_re_no_set_pitch = re.compile(r'\s+A_SetPitch\s*\([\+\w\s\.\+\-\*\\]+\)', re.IGNORECASE)
_re_no_class_replacement = re.compile(r'(actor\s+[\w~.]+\s*:\s*[\w~.]+)\s+replaces\s+[\w~.]+', re.IGNORECASE)
_re_no_doomednum = re.compile(r'(actor\s+[\w~.]+(\s*:\s*[\w~.]+)?\s+(replaces\s+[\w~.]+)?)\s*\d*', re.IGNORECASE)


# Dump all DECORATES before and after patching to two files
_dump_decorates = False

if _dump_decorates:
    import os

    try:
        os.mkdir('tmp')
    except OSError:
        pass

    _original_decos_file = open('tmp/original_decorates.txt', 'wb')
    _processed_decos_file = open('tmp/processed_decorates.txt', 'wb')

def dump_decorate(id, wad, tofile):
    if not tofile:
        return

    decorate = wad.find('DECORATE')
    assert(decorate)

    tofile.write('\n// #{0}: {1}\n\n'.format(id, wad.filename))
    tofile.write(decorate.data)
    tofile.flush()
##    os.fsync(tofile.fileno())


def apply_patch(id, wad):
    if _dump_decorates:
        dump_decorate(id, wad, _original_decos_file)

    # Fix weapon slot and player class resetting
    if id in _broken_keyconfs:
        remove_lump(wad, 'KEYCONF')

    func_name = '_apply_patch_{0}'.format(id)

    if func_name in globals():
        globals()[func_name](wad)

        _verbose_print(VERBOSITY_HIGH, 'Asset-specific patch applied')

    if not allow_set_pitch and id in _weapons_change_pitch:
        replace_in_decorate(wad, _re_no_set_pitch, '')
    if not allow_class_replacement:
        replace_in_decorate(wad, _re_no_class_replacement, r'\1')
    if not allow_doomednum:
        replace_in_decorate(wad, _re_no_doomednum, r'\1')

    make_unique_actors(wad)
    make_unique_sprites(wad)
    make_unique_sounds(wad)

    optimize(wad)

    if _dump_decorates:
        dump_decorate(id, wad, _processed_decos_file)
