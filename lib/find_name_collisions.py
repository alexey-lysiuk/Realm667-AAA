#!/usr/bin/env python

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


"""
 This tool analyzes assets cache or generated .pk3
 for duplicate lump and sprite names within WAD files
 It prints result to stdout in 'known issues' markdown format
"""

import os
import re
import shutil
import zipfile

import doomwad

from case_insensitive import CaseInsensitiveDict
from iwad_lumps import *
from iwad_actors import ACTORS_ALL
from iwad_sndinfo import LOGICAL_SOUNDS_ALL
from iwad_brightmaps import BRIGHTMAPS_ALL
from patching import (
    actor_stateful_pattern, actor_stateless_pattern, actor_header_regex)
import utils


pk3_filename = utils.root_path + 'realm667-aaa.pk3'


excluded_lump_names = [
    # lumps
    'ANIMDEFS',
    'DECALDEF',
    'DECORATE',
    'GLDEFS',
    'KEYCONF',
    'LANGUAGE',
    'LOADACS',
    'LOCKDEFS',
    'SNDINFO',
    'TEXTURES',

    # GLDEFS aliases
    'DOOMDEFS',
    'HTICDEFS',
    'HEXNDEFS',
    'STRFDEFS',

    # markers
    'A_START',
    'A_END',
    'S_START',
    'S_END',
    'SS_START',
    'SS_END',
]

lumps_wads = {}


def find_duplicate_lumps(wad):
    """ Find duplicate lumps in WAD file
        Sprite lumps are not taken into account """
    for namespace in wad.namespaces():
        if doomwad.issrpitenamespace(namespace):
            continue

        for lump in wad.uniquenamespacelumps(namespace):
            if lump.name in excluded_lump_names:
                continue

            if lump.name in lumps_wads \
                    and wad.filename not in lumps_wads[lump.name]:
                lumps_wads[lump.name].append(wad.filename)
            else:
                lumps_wads[lump.name] = [wad.filename]


sprites_wads = {}


def find_duplicate_sprites(wad):
    """ Find duplicate sprites in WAD file (4 characters names) """
    for sprite in wad.spritenames():
        if sprite in sprites_wads:
            sprites_wads[sprite].append(wad.filename)
        else:
            sprites_wads[sprite] = [wad.filename]


actors_wads = CaseInsensitiveDict()


def prepare_decorate(wad):
    decorate = wad.find('DECORATE')

    if not decorate:
        print('No DECORATE lump found in {0}'.format(wad.filename))
        return

    doomwad.striplumpcomments(decorate)
    return decorate.data


def find_duplicate_actors(wad):
    """ Find duplicate actors (classes) in WAD file's DECORATE lump """
    decorate = prepare_decorate(wad)

    if not decorate:
        return

    actors = actor_header_regex.findall(decorate)

    for dummy, actor in actors:
        if actor in actors_wads:
            actors_wads[actor].append(wad.filename)
        else:
            actors_wads[actor] = [wad.filename]


sounds_wads = CaseInsensitiveDict()


def find_duplicate_sounds(wad):
    """ Find duplicate sounds in WAD file's SNDINFO lump """
    sounds = wad.soundmapping(doomwad.SoundMapping.LOGICAL_TO_LUMP)

    for sound in sounds:
        if sound in sounds_wads:
            sounds_wads[sound].append(wad.filename)
        else:
            sounds_wads[sound] = [wad.filename]


def read_wad(zip_file, filename):
    wad_file = zip_file.open(filename)
    wad_data = wad_file.read()
    wad_file.close()

    return doomwad.WadFile(wad_data)


states_block_regex = re.compile(r'states\s+\{(.*?)}', re.IGNORECASE | re.DOTALL)
state_regex = re.compile(r'\s*"?([\w#-]{4})"?\s+"?[\w\[\]\\#]+"?\s+-?\d+')

deco_sprites = {}

# special names, see http://zdoom.org/wiki/Sprite
EXCLUDED_SPRITES = {'####', '----', 'TNT1'}


def gather_sprites(wad):
    decorate = prepare_decorate(wad)

    for states in states_block_regex.findall(decorate):
        for line in states.split('\n'):
            state_match = state_regex.match(line)

            if state_match:
                sprite = state_match.group(1).upper()

                if sprite in EXCLUDED_SPRITES:
                    continue

                wads = deco_sprites.setdefault(sprite, set())
                wads.add(wad.filename)


def print_sprite_usage(iwads, warnings_only=False):
    print('\nSprite usage:')

    for sprite, deco_wads in sorted(deco_sprites.items()):
        wads = []

        if sprite in sprites_wads:
            wads += sprites_wads[sprite]

        from_iwad = False

        for iwad in iwads:
            if sprite in iwad[1]:
                wads.append(iwad[0])
                from_iwad = True

        if not warnings_only or 1 != len(wads) or from_iwad:
            print('{}: stored in {}, referenced from {}'
                  .format(sprite, wads, sorted(deco_wads)))


def print_duplicates(mapping, iwads):
    duplicates = []

    for name, wads in mapping.items():
        wads = wads[:]

        for iwad in iwads:
            if name in iwad[1]:
                wads.append(iwad[0])

        if 1 == len(wads):
            continue

        wads.sort(key=lambda key: key.lower())

        duplicates.append('|{0}|{1}||'.format(name, ', '.join(wads)))

    duplicates.sort()

    for dup in duplicates:
        print(dup)


actor_dump_path = utils.temp_path + 'actors/'


def dump_actor(actor, filename, content):
    dump_filename = '{0}{1}_{2}.txt' \
        .format(actor_dump_path, actor, filename[:-4])

    f = open(dump_filename, 'wb')
    f.write(content)
    f.close()


def dump_duplicate_actors():
    # NOTE: implementation ignores internal ZDoom actors at the moment

    try:
        shutil.rmtree(actor_dump_path)
    except OSError:
        pass

    try:
        os.makedirs(actor_dump_path)
    except OSError:
        pass

    pk3_file = zipfile.ZipFile(pk3_filename)
    count = 0

    for actor in actors_wads:
        wad_names = actors_wads[actor]

        if 1 == len(wad_names):
            continue

        for wad_name in wad_names:
            wad = read_wad(pk3_file, wad_name)
            decorate = prepare_decorate(wad)

            if not decorate:
                continue

            for pattern in (actor_stateless_pattern, actor_stateful_pattern):
                match = re.search(pattern % actor, decorate, re.IGNORECASE | re.DOTALL)

                if match:
                    dump_actor(actor, wad_name, match.group())
                    count += 1
                    break

    print('\nActors written: {0}\n'.format(count))
    pk3_file.close()


def main():
    # Scan generated .pk3

    pk3_file = zipfile.ZipFile(pk3_filename)

    for zipped_filename in pk3_file.namelist():
        if not zipped_filename.lower().endswith('.wad'):
            continue

        wad = read_wad(pk3_file, zipped_filename)
        wad.filename = zipped_filename

        gather_sprites(wad)
        find_duplicate_lumps(wad)
        find_duplicate_sprites(wad)
        find_duplicate_actors(wad)
        find_duplicate_sounds(wad)

    pk3_file.close()

    # Print names collisions

    print('\n|Lump|WAD Files|Comments|\n|---|---|---|')
    print_duplicates(lumps_wads, (
        ('DOOM1', LUMPS_ULTDOOM),
        ('DOOM2', LUMPS_DOOM2),
        ('TNT', LUMPS_TNT),
        ('PLUTONIA', LUMPS_PLUTONIA),
        ('HERETIC', LUMPS_HERETIC),
        ('HEXEN', LUMPS_HEXEN),
        ('STRIFE', LUMPS_STRIFE),
        ('ZDOOM', LUMPS_ZDOOM),
        ('BRIGHTMAPS', BRIGHTMAPS_ALL),
    ))

    sprites_iwads = (
        ('DOOM1', SPRITES_ULTDOOM),
        ('DOOM2/TNT/PLUTONIA', SPRITES_DOOM2),
        ('HERETIC', SPRITES_HERETIC),
        ('HEXEN', SPRITES_HEXEN),
        ('STRIFE', SPRITES_STRIFE),
        ('(G)ZDOOM', SPRITES_ZDOOM),
    )

    print('\n|Sprite|WAD Files|Comments|\n|---|---|---|')
    print_duplicates(sprites_wads, sprites_iwads)

    print('\n|Actor|WAD Files|Comments|\n|---|---|---|')
    print_duplicates(actors_wads, (
        ('ALL GAMES', [name.lower() for name in ACTORS_ALL]),))

    if False:
        print('\n|Sound|WAD Files|Comments|\n|---|---|---|')
        print_duplicates(sounds_wads, (
            ('ALL GAMES', [sound for sound in LOGICAL_SOUNDS_ALL]),))

    if False:
        dump_duplicate_actors()

    if False:
        print_sprite_usage(sprites_iwads, warnings_only=True)


if __name__ == '__main__':
    main()
