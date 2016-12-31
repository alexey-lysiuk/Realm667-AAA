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

import random
import re
import string

import doomwad

from case_insensitive import CaseInsensitiveSet
from iwad_lumps import SPRITES_ALL
from iwad_sndinfo import *


# Allow A_SetPitch() calls in DECORATE,
# suitable for playing with mouselook enabled
allow_set_pitch = False

# Allow class replacement in DECORATE
allow_class_replacement = False

# Allow editor number (doomednum) assignment in DECORATE
allow_doomednum = False

# Enable various WAD files optimizations,
# like removal of unused, duplicate and map lumps
enable_optimization = True

# Convert sprites to PNG format
png_sprites = False
png_sprites_compression = -1


# ==============================================================================


VERBOSITY_NONE = 0
VERBOSITY_LOW = 1
VERBOSITY_HIGH = 2
VERBOSITY_VERY_HIGH = 3


verbosity_level = VERBOSITY_NONE


def _verbose_print(level, message):
    if verbosity_level >= level:
        print(' * {0}'.format(message))


# ==============================================================================


def _replace_in_lump(name, wad, old, new, optional=False):
    lump = wad.find(name)

    if lump:
        if hasattr(old, 'sub') and hasattr(old, 'groups'):
            # regular expression object
            lump.data, count = old.subn(new, lump.data, 0)
            old = old.pattern
        else:
            # string object
            lump.data, count = re.subn(old, new, lump.data, 0, re.IGNORECASE)

        if 0 == count and not optional:
            print('Error: No match found for pattern {} in lump {}'.format(old, name))

        return count

    elif not optional:
        print("Error: Cannot find lump {0}".format(name))

    return 0


def _replace_in_decorate(wad, old, new, optional=False):
    _replace_in_lump('DECORATE', wad, old, new, optional)


def _replace_in_gldefs(wad, old, new, optional=False):
    count = 0

    for alias in ('GLDEFS', 'DOOMDEFS', 'HTICDEFS', 'HEXNDEFS', 'STRFDEFS'):
        count += _replace_in_lump(alias, wad, old, new, optional=True)

    if 0 == count and not optional:
        print("Error: Failed to find pattern in GLDEFS")


def _replace_in_sndinfo(wad, old, new, optional=False):
    _replace_in_lump('SNDINFO', wad, old, new, optional)


def _rename_lump(wad, old, new):
    lump = wad.find(old)

    if lump:
        lump.name = new

        _verbose_print(
            VERBOSITY_LOW, 'Lump {0} was renamed to {1}'.format(old, new))
    else:
        print('Error: Cannot find lump {0}'.format(old))


def _add_lump(wad, name, content):
    lump = wad.find(name)

    if lump:
        print('Error: Lump {0} is already exist'.format(name))
    else:
        lump = doomwad.Lump(name, content)
        wad.append(lump)

        _verbose_print(
            VERBOSITY_LOW, 'Lump {0} was added'.format(name))


def _remove_lump(wad, name):
    lump = wad.find(name)

    if lump:
        wad.removelump(lump)

        _verbose_print(
            VERBOSITY_LOW, 'Lump {0} was deleted'.format(name))
    else:
        print("Error: Cannot find lump {0}".format(name))


def _remove_lumps(wad, pattern):
    lumps = []

    for lump in wad:
        if re.match(pattern, lump.name):
            lumps.append(lump)

    for lump in lumps:
        wad.removelump(lump)

        _verbose_print(VERBOSITY_LOW, 'Lump {0} was deleted'.format(lump.name))


def _remove_unused_sound(wad, lump_name):
    sndinfo = wad.find('SNDINFO')
    if sndinfo:
        if lump_name not in sndinfo.data:
            _remove_lump(wad, lump_name)


def optimize_text(text):
    lines = text.split('\n')

    lines = [line.strip() for line in lines]
    lines = [re.sub('\s+', ' ', line) for line in lines
             if line and not line.startswith('//')]

    return '\n'.join(lines)


def _optimize_text_lump(wad, name):
    lump = wad.find(name)

    if lump:
        lump.data = optimize_text(lump.data)


# ==============================================================================


# the following dictionary in the same format as returned from WadFile.spritemapping()
# single incorrect frame is added for all sprites,
# so sprites from IWADs will always be different and
# any possibility of name collision is avoided
_sprites = {sprite: {None: None} for sprite in SPRITES_ALL}


def _generate_unique_sprite_name(sprite, frames):
    name_chars = string.ascii_uppercase + string.digits
    char_count = len(name_chars)

    name_length = len(sprite)

    while True:
        unique_name = ''

        for i in range(name_length):
            index = random.randrange(0, char_count)
            unique_name += name_chars[index]

        if unique_name not in _sprites:
            _sprites[unique_name] = frames
            return unique_name

    assert False
    return None


_sprites_renames = {}


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


def _rename_sprite(wad, old, new):
    search_pattern = r'(\s"?)%s("?\s+"?[\[\]\w\\]+"?\s+-?\d)' % old
    replace_pattern = r'\g<1>{0}\g<2>'.format(new)

    decorate = wad.find('DECORATE')
    assert decorate

    decorate.data, count = re.subn(
        search_pattern, replace_pattern, decorate.data, 0, re.IGNORECASE)

    search_pattern = r'Inventory.Icon\s+"?(%s\w{0,4})"?[\s}]' % old

    for icon in re.findall(search_pattern, decorate.data, re.IGNORECASE):
        icon_lump = wad.find(icon)

        search_pattern = r'(Inventory.Icon\s+"?)%s(\w{0,4}"?[\s}])' % old

        if icon_lump and doomwad.issrpitenamespace(icon_lump.namespace):
            decorate.data, icount = re.subn(
                search_pattern, replace_pattern, decorate.data, 0,
                re.IGNORECASE)
            count += icount

    if 0 == count:
        _verbose_print(VERBOSITY_VERY_HIGH, 'Found unused sprite ' + old)

    search_pattern = r'([\s"])%s(\w{0,4}[\s"])' % old

    _replace_in_lump(
        'ANIMDEFS', wad, search_pattern, replace_pattern, optional=True)
    _replace_in_lump(
        'DECALDEF', wad, search_pattern, replace_pattern, optional=True)
    _replace_in_gldefs(
        wad, r"frame\s*" + search_pattern, "frame " + replace_pattern, optional=True)

    for lump in wad.spritelumps():
        if lump.name.startswith(old):
            lump.name = new + lump.name[4:]

    if old in _sprites_renames:
        _sprites_renames[old].append(new)
    else:
        _sprites_renames[old] = [new]

    _verbose_print(
        VERBOSITY_LOW,
        'Sprite {0} was renamed to {1}'.format(old, new))


def _make_unique_sprites(wad):
    """ Find and rename sprites with the same name but different content
        New names are randomly generated """

    # very special case:
    # if keep_sprites attribute exists in wad instance,
    # ignore possible sprite name collision and keep the name unchanged
    # for example, when sprite from IWAD is extended with frames from PWAD
    keep_sprites = hasattr(wad, 'keep_sprites') and wad.keep_sprites or ()

    for name, frames in wad.spritemapping().items():
        if name in keep_sprites:
            continue

        if name in _sprites:
            if frames != _sprites[name]:
                new_name = _generate_new_sprite_name(name, frames)
                _rename_sprite(wad, name, new_name)
        else:
            _sprites[name] = frames


# ==============================================================================


_actors = CaseInsensitiveSet()


def _rename_actor(wad, actor):
    new_name = '????'
    suffix = 1

    # generate unique actor name
    while True:
        new_name = '{0}_{1}'.format(actor, suffix)

        if new_name not in _actors:
            _actors.add(new_name)
            break

        suffix += 1

    # replace old name
    old_pattern = r'(["\s]){0}(["\s:])'.format(actor)
    new_pattern = r'\g<1>{0}\g<2>'.format(new_name)

    _replace_in_decorate(wad, old_pattern, new_pattern)
    _replace_in_gldefs(wad, old_pattern, new_pattern, optional=True)

    _verbose_print(
        VERBOSITY_LOW,
        'Actor class {0} was renamed to {1}'.format(actor, new_name))


# TODO: is it ever possible to do this using ONE regex?
actor_stateful_pattern = r'actor\s+%s[\s:{].*?(states\s*{.+?}).*?}\s*'
actor_stateless_pattern = r'actor\s+%s[\s:{].*?}\s*'


def _remove_actor(decorate, name):
    count_total = 0

    for pattern in (actor_stateful_pattern, actor_stateless_pattern):
        decorate.data, count = re.subn(
            pattern % name, '', decorate.data, 0,
            re.IGNORECASE | re.DOTALL)
        count_total += count

    if 0 == count_total:
        print('Error: Failed to delete actor class ' + name)
    else:
        _verbose_print(VERBOSITY_LOW, 'Actor class {} was deleted'.format(name))


actor_header_regex = re.compile(
    r'(\s|^)actor\s+([\w+~.]+).*?{', re.IGNORECASE | re.DOTALL)

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


def _make_unique_actors(wad):
    decorate = wad.find('DECORATE')
    assert decorate

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
                _remove_actor(decorate, actor)
            else:
                _rename_actor(wad, actor)
        else:
            _actors.add(actor)


# ==============================================================================


_lumps = {}

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
    'CREDITS',   # informational
    'DOCUMENT',  # informational
    'INFO',      # informational
    'MAPINFO',   # not needed, maps are removed during optimization
    'README',    # informational
    'RELOADIN',  # alternative DECORATE lumps
    'UPDATES',   # informational
    '--------',
}


def _is_lump_needed(lump):
    name = lump.name

    if name in _excluded_names:
        _verbose_print(
            VERBOSITY_HIGH,
            'Unwanted lump {0} was deleted'.format(name))
        return False

    if lump.marker or name in _included_names:
        return True

    checksum = lump.hash()

    if name in _lumps:
        if checksum in _lumps[name]:
            _verbose_print(
                VERBOSITY_HIGH,
                'Duplicate lump {0} was deleted'.format(name))
            return False
        else:
            _lumps[name].add(checksum)
            return True
    else:
        _lumps[name] = {checksum}
        return True


def _optimize(wad):
    # remove map lumps
    while True:
        things_lump = wad.find('THINGS')
        if not things_lump:
            break

        map_name = things_lump.namespace
        wad.filter(lambda lump: map_name != lump.name
                   and map_name != lump.namespace)

    # remove other unwanted lumps
    wad.filter(_is_lump_needed)

    # optimize common text lumps
    _optimize_text_lump(wad, 'DECORATE')
    _optimize_text_lump(wad, 'GLDEFS')
    _optimize_text_lump(wad, 'SNDINFO')


# ==============================================================================


def _generate_unique_lump_name():
    name_chars = string.ascii_uppercase + string.digits + '_'
    char_count = len(name_chars)

    while True:
        unique_name = ''

        for i in range(8):
            index = random.randrange(0, char_count)
            unique_name += name_chars[index]

        if unique_name not in _lumps:
            return unique_name

    assert False
    return None


# ==============================================================================


# map sound lump names to a hash of lump's content
_sound_lumps = {name: None for name in SOUNDS_LUMPS_ALL}

# map old names to a set of new names
_sound_lump_renames = {}


def _rename_sound_lump(wad, name, content_hash):
    """ Rename sound lump in WAD file and change references to it in SNDINFO """

    # if keep_sound_lumps attribute exists in wad instance
    # keep the name unchanged and ignore possible name
    keep_sound_lumps = hasattr(wad, 'keep_sound_lumps') and wad.keep_sound_lumps or ()

    if name in keep_sound_lumps:
        return

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

    _rename_lump(wad, name, new_name)
    _replace_in_sndinfo(
        wad,
        r'(\s){0}(\s|$)'.format(name),
        r'\g<1>{0}\g<2>'.format(new_name))


_rename_sound_lump.mapping_type = doomwad.SoundMapping.LUMP_TO_CONTENT
_rename_sound_lump.global_mapping = _sound_lumps


# map logical sound name to a lump name, based on SNDINFO lump content
_logical_sounds = {name: None for name in LOGICAL_SOUNDS_ALL}


def _rename_logical_sound(wad, logical_name, lump_name):
    """ Rename logical sound in SNDINFO lump and change references to it in DECORATE """

    # if keep_logical_sounds attribute exists in wad instance
    # keep the name unchanged and ignore possible name
    keep_logical_sounds = hasattr(wad, 'keep_logical_sounds') and wad.keep_logical_sounds or ()

    if logical_name in keep_logical_sounds:
        return

    new_name = 'r667aaa/' + _generate_unique_lump_name().lower()
    _logical_sounds[new_name] = lump_name

    _replace_in_decorate(
        wad,
        '"{0}"'.format(logical_name),
        '"{0}"'.format(new_name))
    _replace_in_sndinfo(
        wad,
        r'(^|\s){0}(\s)'.format(logical_name),
        r'\g<1>{0}\g<2>'.format(new_name))

    _verbose_print(
        VERBOSITY_LOW,
        'Logical sound {0} was renamed to {1}'.format(logical_name, new_name))

    return new_name


_rename_logical_sound.mapping_type = doomwad.SoundMapping.LOGICAL_TO_LUMP
_rename_logical_sound.global_mapping = _logical_sounds


def _make_unique_sounds_with_mapping(wad, rename_func):
    mapping = wad.soundmapping(rename_func.mapping_type)

    for key in mapping:
        value = mapping[key]

        if value and key in rename_func.global_mapping:
            if value != rename_func.global_mapping[key]:
                rename_func(wad, key, value)
        else:
            rename_func.global_mapping[key] = value


def _make_unique_sounds(wad):
    _make_unique_sounds_with_mapping(wad, _rename_sound_lump)
    _make_unique_sounds_with_mapping(wad, _rename_logical_sound)


# ==============================================================================

# Asset-specific patches

def _apply_patch_10(wad):  # Apprentice of D'Sparil
    # fix missing marker
    sprite_end_marker = 'S_END'
    if not wad.find(sprite_end_marker):
        marker = doomwad.Lump(sprite_end_marker, '')
        wad.append(marker)


def _apply_patch_14(wad):  # Bat
    # remove sprites with broken transparency
    # lumps from #185 Baphomet's Eyes will be used
    # they are the same sprites but with correct alpha channel
    wad.removesprite('BFAM')


def _apply_patch_33(wad):  # Darkness Rift
    # fix wrong class name
    _replace_in_decorate(wad, '"Fatty"', '"Fatso"')


def _apply_patch_38(wad):  # Diabolist
    # do not rename sprites from Hexen
    wad.keep_sprites = ('CFCF', 'CFFX')

    # do not rename logical sounds from Hexen
    wad.keep_logical_sounds = (
        'clericflamecircle',
        'clericflameexplode',
        'clericflamefire'
    )

def add_dummy_brighmap(wad, name):
    # fix 'brightmap not found' warning in console
    brightmap = doomwad.Lump(
        name,
        # 16x16 pixels image filled with black in PNG format
        '\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52'
        '\x00\x00\x00\x10\x00\x00\x00\x10\x08\x04\x00\x00\x00\xb5\xfa\x37'
        '\xea\x00\x00\x00\x15\x49\x44\x41\x54\x28\xcf\x63\x64\xf8\xcf\x80'
        '\x17\x30\x31\x30\x8c\x2a\x18\x39\x0a\x00\x2f\x20\x01\x1f\x24\xfd'
        '\x05\xb8\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82')
    wad.append(brightmap)


def _apply_patch_40(wad):  # Double Chaingunner
    add_dummy_brighmap(wad, 'BMDPOSE5')


def _apply_patch_44(wad):  # Fallen
    add_dummy_brighmap(wad, 'BMFALNM0')


def _apply_patch_52(wad):  # Hell Apprentice
    _remove_unused_sound(wad, 'DSDASH')


def _apply_patch_55(wad):  # Hell Smith
    _remove_unused_sound(wad, 'DSDASH')


def _fix_actor_borgnail2(wad):
    # fix wrong class name
    _replace_in_decorate(wad, '"BornNail2"', '"BorgNail2"')


def _apply_patch_66(wad):  # Nail Borg
    _fix_actor_borgnail2(wad)


def _apply_patch_70(wad):  # Nightmare Demon
    # fix brightmap collisions with #17 Blood Fiend
    for lump in wad:
        if lump.name.startswith('BMSAR2'):
            lump.name = 'BMNMDM' + lump.name[6:]
    _replace_in_gldefs(wad, r'(\s)BMSAR2(\w{2}\s)', r'\1BMNMDM\2')


def _apply_patch_71(wad):  # Plasma Demon
    # resolve sound lumps conflicts with Doom IWADs
    sndinfo = wad.find('SNDINFO')
    if sndinfo:
        sndinfo.data += 'blueball/attack DSFIRSHT\n' \
                        'blueball/shotx  DSFIRXPL\n'
        _replace_in_decorate(
            wad,
            r'(Sound\s")imp(/\w+")',
            r'\1blueball\2')


def _apply_patch_151(wad):  # Phantom
    # fix wrong class name
    _replace_in_decorate(wad, '"GhostHatch"', '"PhantomHatch"')


def _apply_patch_228(wad):  # Zombieman Rifle
    # fix class name collision with #407 Rifle
    _replace_in_decorate(
        wad,
        r'(actor\s+)Rifle(\s*:\s*\w+)',
        r'\1ZombiemanRifle\2')


def _fix_raduis_quake(wad):
    # remove quake sound override
    _replace_in_sndinfo(wad, r'world/quake\s+(""|none)', '')

    # replace Radius_Quake() with A_Quake()
    decorate = wad.find('DECORATE')
    assert decorate

    raduis_quake_pattern = re.compile(r'(radius_quake\s*\((\s*\d+),(\s*\d+),(\s*\d+),(\s*\d+),\s*\d+\))', re.IGNORECASE)
    functions = raduis_quake_pattern.findall(decorate.data)

    if 0 == len(functions):
        print('Error: No match found for Radius_Quake() pattern')
        return

    for func in functions:
        assert 5 == len(func)

        intensity = int(func[1])
        duration = int(func[2])
        damrad = int(func[3]) * 64
        tremrad = int(func[4]) * 64

        a_quake = 'A_Quake({}, {}, {}, {}, "")'.format(intensity, duration, damrad, tremrad)
        decorate.data = decorate.data.replace(func[0], a_quake)


def _apply_patch_233(wad):  # Machinegun
    _fix_raduis_quake(wad)


def _apply_patch_241(wad):  # Devastator
    # fix incorrect sprite
    _replace_in_decorate(wad, r'(\s)DVST(\s)', r'\1DVGG\2')


def _apply_patch_242(wad):  # Freeze Rifle
    # fix incorrect sprite
    _replace_in_decorate(wad, r'(\s)PLSG(\s)', r'\1FRSG\2')


def _apply_patch_256(wad):  # Mancubus Arm
    # fix incorrect inventory class
    _replace_in_decorate(wad, r'(A_GiveInventory\s*\(\s*")(Blood")', r'\1Demon\2')


def _apply_patch_258(wad):  # Poly Morph
    # do not rename sprites from Heretic and Hexen
    wad.keep_sprites = ('CHKN', 'PIGY', 'BEAK', 'WPIG')

    # do not rename logical sounds from Heretic and Hexen
    wad.keep_logical_sounds = (
        'chicken/active',
        'chicken/attack',
        'chicken/death',
        'chicken/pain',
        'chicken/peck',
        'pigactive1',
        'pigactive2',
        'pigattack',
        'pigdeath',
        'pigpain'
    )


def _apply_patch_266(wad):  # Napalm Launcher
    # remove unused sprites
    _remove_lumps(wad, 'FSPK[A-E]0')
    _remove_lumps(wad, 'SMOK[A-Q]0')


def _apply_patch_271(wad):  # Saw Thrower
    # fix incorrect sprite
    _replace_in_decorate(
        wad,
        r'Inventory.Icon(\s+)SAWA',
        r'Inventory.Icon\1SAWAA0')


def _apply_patch_272(wad):  # Sniper Rifle
    # remove unused sprites
    _remove_lumps(wad, 'BULL[A-F]0')


def _apply_patch_284(wad):  # Arachnobaron
    add_dummy_brighmap(wad, 'BMARBRB5')


def _apply_patch_308(wad):  # Doom III Super Shotgun
    # fix sound and sprite name collisions with Doom II Super Shotgun
    _replace_in_decorate(
        wad,
        r'(\w+\s+\w\s+)(\d+\s+)(\w*\s*)A_FireShotgun2',
        '\\g<1>0 \\3A_FireBullets(11.2, 7.1, 20, 5, "BulletPuff")\n'
        '      \\g<1>0 \\3A_PlaySound("doom3ssg/fire", CHAN_WEAPON)\n'
        '      \\g<1>\\2\\3A_GunFlash')
    _replace_in_decorate(
        wad,
        r'(\w+\s+\w\s+\d+\s+\w*\s*)A_OpenShotgun2',
        r'\1A_PlaySound("doom3ssg/open", CHAN_WEAPON)')
    _replace_in_decorate(
        wad,
        r'(\w+\s+\w\s+\d+\s+\w*\s*)A_LoadShotgun2',
        r'\1A_PlaySound("doom3ssg/load", CHAN_WEAPON)')
    _replace_in_decorate(
        wad,
        r'(\w+\s+\w\s+\d+\s+\w*\s*)A_CloseShotgun2',
        r'\1A_PlaySound("doom3ssg/close", CHAN_WEAPON)')
    _replace_in_decorate(
        wad,
        r'Stop(\s+)}(\s+)}',
        'Stop\n   Spawn:\n      SG3W A -1\n      Stop\\1}\\2}')

    _rename_lump(wad, 'SGN2A0',   'SG3WA0'  )
    _rename_lump(wad, 'DSDSHTGN', 'SSG3FIRE')
    _rename_lump(wad, 'DSDBLOAD', 'SSG3LOAD')
    _rename_lump(wad, 'DSDBOPN',  'SSG3OPEN')
    _rename_lump(wad, 'DSDBCLS',  'SSG3CLOS')

    _add_lump(
        wad, 'SNDINFO',
        'doom3ssg/fire  SSG3FIRE\n'
        'doom3ssg/load  SSG3LOAD\n'
        'doom3ssg/open  SSG3OPEN\n'
        'doom3ssg/close SSG3CLOS\n')


def _apply_patch_314(wad):  # Revolver PS
    # fix incorrect sprite
    _replace_in_decorate(wad, r'HGUN(\s+)A(\s+)1', r'HGUN\1C\2-1')


def _apply_patch_316(wad):  # Agaures
    add_dummy_brighmap(wad, 'BMAGURG5')


def _apply_patch_318(wad):  # Moloch
    # fix usage of missing actor class
    _replace_in_decorate(
        wad,
        r'(\w+\s+\w\s+\d\s+A_CustomMissile\s*\(\s*"MolochDeathFire")',
        r'//\1')


def _apply_patch_337(wad):  # Nail Borg Commando
    _fix_actor_borgnail2(wad)


def _apply_patch_380(wad):  # Shrink Sphere
    # disable morph style flag unsupported in ZDoom 2.8.1
    # TODO: remove this "fix" after 2.9 release
    _replace_in_decorate(
        wad,
        r'(PowerMorph.MorphStyle\s*\(?MRF_TRANSFERTRANSLATION\)?)',
        r'/*\1*/')


def _apply_patch_405(wad):  # Impaled Rocket Guy
    # fix wrong sprite name
    _rename_lump(wad, 'IMRGA1', 'IMRGA0')


def _apply_patch_409(wad):  # Duke Shotgun
    _fix_raduis_quake(wad)


def _apply_patch_412(wad):  # Power Stimpack
    # fix wrong class name
    _replace_in_gldefs(wad, r'(\s)PowerStimpack(\s)', r'\1PowerStim\2')


def _apply_patch_421(wad):  # Switchable Tech Lamp
    # extend sprite from Doom II and Final Doom IWADs
    if wad.find('TLMPE0'):
        wad.keep_sprites = ('TLMP',)


def _apply_patch_433(wad):  # Chiller
    # fix missing class name
    _replace_in_decorate(wad, '"ChillerFog2"', '"ChillerFog"')


_gizmo_search_pattern = r'(\sBlue|Red|Yellow)(Key|Skull)Gizmo(\s)'


def _apply_patch_474(wad):  # Hell Gizmos
    # fix class name collisions with #476 Tech Gizmos
    # do not rely on automatic conflict resolution,
    # as these actors are explicitly referenced from menu
    _replace_in_decorate(wad, _gizmo_search_pattern, r'\1\2HellGizmo\3')


def _apply_patch_476(wad):  # Tech Gizmos
    # fix class name collisions between two versions
    # and also with #476 Tech Gizmos
    # do not rely on automatic conflict resolution,
    # as these actors are explicitly referenced from menu
    if '1' in wad.filename:
        # fire version
        _replace_in_decorate(wad, _gizmo_search_pattern, r'\1\2FireGizmo\3')
    elif '2' in wad.filename:
        # sphere version
        _replace_in_decorate(wad, _gizmo_search_pattern, r'\1\2SphereGizmo\3')


def _apply_patch_485(wad):  # Talisman of the Depths
    # fix class name collision with #482 Rebreather
    # cannot be resolved automatically because of optional Power... prefix
    _replace_in_decorate(wad, r'NoDrown(\s+)', r'NoDrownTalisman\1')


def _apply_patch_511(wad):  # Lightbringer'
    # fix wrong class and light names
    _replace_in_gldefs(wad, r'(\s)SunProjectile1(\s)', r'\1SunProjectile\2')


def _apply_patch_536(wad):  # Jackbomb
    # fix missing class reference
    regex = re.compile(
        r'object\s+Curse\s+\{.*?\s+\}\s+}\s*',
        re.IGNORECASE | re.DOTALL)
    _replace_in_gldefs(wad, regex, '')


def _apply_patch_543(wad):  # UTNT Pyro-Cannon...
    # remove unused sprites
    _remove_lumps(wad, 'AGAS[AB]0')


def _apply_patch_558(wad):  # Various Doom Keys
    # fix lump names collision with graphics from (G)ZDoom
    for i in range(6, 9):
        old_name = 'STKEYS{}'.format(i)
        new_name = old_name + '_'

        _replace_in_decorate(wad, old_name, new_name)
        _rename_lump(wad, old_name, new_name)


def fix_always_activate(wad):
    # fix incorrect inventory flag
    _replace_in_decorate(
        wad,
        'Inventory.AlwaysActivate',
        'Inventory.AutoActivate')


def _apply_patch_577(wad):  # Guard Sphere
    fix_always_activate(wad)


def _apply_patch_579(wad):  # Time Freeze Sphere
    fix_always_activate(wad)


def _apply_patch_582(wad):  # Super Crossbow
    # fix missing marker
    sprite_end_marker = 'SS_END'
    if not wad.find(sprite_end_marker):
        marker = doomwad.Lump(sprite_end_marker, '')
        wad.append(marker)

    # avoid renaming of ethereal arrow sprites from Heretic
    if wad.find('FX03A1'):
        wad.keep_sprites = ('FX03',)

def _apply_patch_604(wad):  # Dark Inquisitor
    # fix lump name conflict with Doom IWADs
    _rename_sound_lump(wad, 'STEP2', None)


def _apply_patch_620(wad):  # Chesire Cacodemon
    # fix wrong class names
    _replace_in_gldefs(wad, r'(\s)CheshBall(\s)', r'\1ChesBallA\2')


def _apply_patch_647(wad):  # Light Column Variations
    # fix class name collisions with embedded actors
    _replace_in_decorate(wad, r'(\s+)(\w+Column\s+)', r'\1Light\2')


def _apply_patch_659(wad):  # Pulse Rifle UAC
    # fix class name collision with #522 Pulse Rifle
    _replace_in_decorate(
        wad,
        r'(actor\s+)PulseRifle(\s*:\s*\w+)',
        r'\1PulseRifleUAC\2')


def _apply_patch_664(wad):  # Magic Sparkle
    # fix class name collision with #277 Sparkle Spawners
    _replace_in_decorate(
        wad,
        r'([\s:]\w+)SparkleSpawner(\s|:)',
        r'\1MagicSparkle\2')


def _apply_patch_671(wad):  # Food Barrel
    # fix class name collisions with embedded actors
    _replace_in_decorate(wad, 'Meat1', 'MeatBeef')
    _replace_in_decorate(wad, 'Meat2', 'MeatCheese')
    _replace_in_decorate(wad, 'Meat3', 'MeatFish')


def _apply_patch_685(wad):  # Ammo Satchels
    # fix class name collision with ammo from Strife
    _replace_in_decorate(wad, 'AmmoSatchel', 'AmmoSatchelR667')


def _apply_patch_762(wad):  # Model 1887
    # fix wrong end marker
    _rename_lump(wad, 'SS_STOP', 'SS_END')


def _apply_patch_767(wad):  # Strife Pistol
    # convert into generic weapon
    _replace_in_decorate(wad, r'(\s+)StrifeWeapon(\s+)', r'\1Weapon\2')
    _replace_in_decorate(wad, r'(\s+)Game\s+Strife(\s+)', r'\1Weapon.Kickback 100\2')
    _replace_in_decorate(wad, r'(\s+Weapon.AmmoType\s+")ClipOfBullets("\s+)', r'\1Clip\2')


def _apply_patch_795(wad):  # Missile Pod
    # fix usage of missing actor class
    _replace_in_decorate(
        wad,
        r'(\w+\s+\w\s+\d\s+A_SpawnItemEx\s*\(\s*"MissileFlameTrail")',
        r'//\1')


def _apply_patch_801(wad):  # Candle Color Variations
    # fix wrong sprite name
    _rename_lump(wad, 'CNUNA0', 'CNBKA0')


def _apply_patch_802(wad):  # Former Scientists Pack
    # keep sound lumps stored by multiple WADs
    wad.keep_sound_lumps = (
        'DSKNIFE',
        'FEMZACT',
        'FEMZPAIN',
        'FEMZDHT',
        'FEMZDT2',
        'FEMZSIT',
        'FEMZSI2'
    )

    # keep logical sounds defined in multiple WADs
    wad.keep_logical_sounds = (
        'fem/sight1',
        'fem/sight2',
        'fem/pain',
        'fem/death1',
        'fem/death2',
        'fem/active',
        'knifehit'
    )


def _apply_patch_804(wad):  # Light Machinegun
    # fix class name collision with #233 Machinegun
    _replace_in_decorate(
        wad,
        r'(actor\s+)Machinegun(\s*:\s*\w+)',
        r'\1LightMachinegun\2')


def _apply_patch_817(wad):  # Arbalest of the Ancients
    # fix class name collision with #582 Super Crossbow
    _replace_in_decorate(
        wad,
        r'([^\w])SuperCrossbow',
        r'\1Arbalest')


def _apply_patch_865(wad):  # Former Scientists Pack 2
    # the same as for the first pack
    _apply_patch_802(wad)


def _apply_patch_993(wad):  # Sentient Mushroom
    # remove duplicate Big Red Mushroom actor to use the class defined in #613 Mushrooms
    # to use this actor delete the patch and add 'BigMushroomRed' to _duplicate_actors set
    _replace_in_decorate(
        wad,
        r'actor\s+BigMushroomRed\s*{[^{]+{[^{]+}\s*}',
        '')


# ==============================================================================


# Dump all DECORATES before and after patching to two files
_decorates_dumping = False

if _decorates_dumping:
    _original_decos_file = open('tmp/original_decorates.txt', 'wb')
    _processed_decos_file = open('tmp/processed_decorates.txt', 'wb')


def _dump_decorate(gid, wad, tofile):
    if not tofile:
        return

    decorate = wad.find('DECORATE')
    assert decorate

    tofile.write('\n// #{0}: {1}\n\n'.format(gid, wad.filename))
    tofile.write(decorate.data)
    tofile.flush()


# ==============================================================================


_broken_keyconfs = (
    226,  # Sawed Off
    235,  # Uber Minigun
    240,  # Seeker Bazooka
    241,  # Devastator
    246,  # EgoSmasher
    252,  # Tesla Cannon
    257,  # Power Nailgun
    263,  # Hunter Shotgun
    267,  # Necrovision MG40
    269,  # Pulse Machinegun
    273,  # Swat Shotgun
    274,  # Western Shotgun
    283,  # TommyGun
    308,  # Doom 2.5 SSG
    314,  # Revolver PS
    328,  # Spellbinder
    329,  # Plasma Shotgun
    330,  # Butchergun Chaingun
    465,  # Salvation Sphere
    509,  # Prox Launcher
    510,  # Vile Staff
    521,  # Mag .60
    536,  # Jackbomb
    539,  # Blood Lich
    552,  # Hierophant
    626,  # D'sparil Staff
)

# list of weapons with A_SetPitch() call(s) in DECORATE
# These weapons change player's pitch preventing smooth playing
# without mouselook and so they are in the following list
# Some weapons modify player's pitch but then restore it back
# These weapons are commented out in the following list

_weapons_change_pitch = (
    432,  # Autogun
    # 0445,  # Coachgun
    # 0513,  # Smasher
    559,  # Glock 18
    585,  # AA12 Shotgun
    # 599,  # MP40
    600,  # M40A1 Sniper Rifle
    684,  # MP5
    686,  # G3
    719,  # Hunting Rifle
)


_re_no_set_pitch = re.compile(r'\s+A_SetPitch\s*\([\+\w\s\.\-\*\\]+\)', re.IGNORECASE)
_re_no_class_replacement = re.compile(r'(actor\s+[\w~.]+\s*:\s*[\w~.]+)\s+replaces\s+[\w~.]+', re.IGNORECASE)
_re_no_doomednum = re.compile(r'(actor\s+[\w~.]+(\s*:\s*[\w~.]+)?\s+(replaces\s+[\w~.]+)?)\s*\d*', re.IGNORECASE)


def apply_patch(gid, wad):
    if _decorates_dumping:
        _dump_decorate(gid, wad, _original_decos_file)

    # fix conflict with texture from IWADs
    credit_lump = wad.find('CREDIT')
    if credit_lump:
        credit_lump.name = 'CREDITS'

    # Fix weapon slot and player class resetting
    if gid in _broken_keyconfs:
        _remove_lump(wad, 'KEYCONF')

    func_name = '_apply_patch_{0}'.format(gid)

    if func_name in globals():
        globals()[func_name](wad)

        _verbose_print(VERBOSITY_HIGH, 'Asset-specific patch applied')

    if not allow_set_pitch and gid in _weapons_change_pitch:
        _replace_in_decorate(wad, _re_no_set_pitch, '', optional=True)
    if not allow_class_replacement:
        _replace_in_decorate(wad, _re_no_class_replacement, r'\1', optional=True)
    if not allow_doomednum:
        _replace_in_decorate(wad, _re_no_doomednum, r'\1', optional=True)

    _make_unique_actors(wad)
    _make_unique_sprites(wad)
    _make_unique_sounds(wad)

    if enable_optimization:
        _optimize(wad)

    if png_sprites:
        from doompic import doompic_to_png

        for sprite in wad.spritelumps():
            if sprite.data.startswith('\x89PNG'):
                continue
            sprite.data = doompic_to_png(sprite.rawdata, png_sprites_compression)

            _verbose_print(
                VERBOSITY_VERY_HIGH, 'Sprite {0} converted to PNG format'.format(sprite.name))

    if _decorates_dumping:
        _dump_decorate(gid, wad, _processed_decos_file)
