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

import cStringIO
import os, sys
import urllib2
import zipfile

sys.path.append(os.path.dirname(__file__) + '/lib')

import doomwad
import patching

# Configuration

repository = [
    # Armory

    # Doom Style
    (342, '40mm Grenade Launcher'),
    (585, 'AA12 Shotgun'),
    (260, 'Action Machine Gun'),
    (516, 'AK47'),
    (685, 'Ammo Satchels'),
    (534, 'Angled Pistol'),
    (432, 'Autogun'),
    (884, 'Axe'),
    (372, 'BFG10K'),
    (874, 'BFG 2704'),
    (281, 'Bio Pipebomb Launcher'),
    (903, 'Black Hole Generator'),
    (330, 'Butcher Chaingun'),
    (403, 'Channeler Plasma Rifle'),
    (758, 'Claymore Mines'),
    (445, 'Coachgun'),
    (581, 'Colt 45'),
    (816, 'Cryobow'),
    (308, 'Doom 2.5 Super Shotgun'),
    (520, 'Double Bladed Chainsaw'),
    (344, 'Double Grenade Launcher'),
    (409, 'Duke Shotgun'),
    (246, 'EgoSmasher'),
    (262, 'Electro Gun'),
    (507, 'Fist Redux'),
    (541, 'Flamethrower'),
    (913, 'Flashlight'),
    (242, 'Freeze Rifle'),
    (559, 'Glock 18'),
    (373, 'Grenade Launcher'),

    # Other Sources / Styles
    (408, 'Drummle Auto-Shotgun'),

    # Beastiary
    (  7, 'Afrit'),
    (  8, 'Agathodemon'),
    (316, 'Agaures'),
    (  9, 'Annihilator'),
    (284, 'Arachnobaron'),
    ( 11, 'Arachnophyte'),
    (285, 'Aracnorb'),
    ( 12, 'Archon of Hell'),
    (768, 'Augmented Arachnotron'),
    (555, 'Auto Shotgun Guy'),
    (148, 'Azazel'),
    (877, 'Baby Cacodemon'),
    ( 15, 'Belphegor'),

    # Items
    (490, 'Adrenaline Kit'),
    (897, 'Familiar Summon'),
    (898, 'Ritual Knife'),
    (926, 'Shield Spells'),
]

output_filename = 'realm667-aaa.pk3'

url_download = 'http://realm667.com/index.php/en/component/docman/?task=doc_download&gid={0}'


def prepare():
    try:
        os.remove(output_filename)
    except OSError:
        # TODO: report error
        pass

    try:
        os.mkdir('cache')
    except OSError:
        # TODO: report error
        pass

def add_lump(zip, filename):
    zip.write('dat/{0}'.format(filename), filename)


def main():
    prepare()

    # TODO: add error handling
    output_file = zipfile.ZipFile(output_filename, 'a', zipfile.ZIP_DEFLATED)

    for item in repository:
        id   = item[0]
        name = item[1]

        print('Processing #{:04d}: {:s}...'.format(id, name))

        cached_filename = 'cache/{:04d}.zip'.format(id)
        cached_file = None

        try:
            cached_file = zipfile.ZipFile(cached_filename, 'r')

        except Exception:
            try:
                url = url_download.format(id)
                response = urllib2.urlopen(url)
                data = response.read()

                # TODO: add error handling
                with open(cached_filename, 'wb') as cached_file:
                    cached_file.write(data)

                cached_file = zipfile.ZipFile(cached_filename, 'r')

            except Exception:
                # TODO: report error
                continue

        wad_filenames = []

        for zipped_filename in cached_file.namelist():
            if zipped_filename.lower().endswith('.wad'):
                wad_filenames.append(zipped_filename)

        if 0 == len(wad_filenames):
            cached_file.close()

            print('Error: no WAD files found')
            continue

        for filename in wad_filenames:
            try:
                wad_file = cached_file.open(filename)
                wad_data = wad_file.read()
                wad_file.close()

                wad = doomwad.WadFile(wad_data)

                if not wad.find('DECORATE'):
                    print('Warning: No DECORATE lump found in file {0}, skipping...'.format(filename))
                    continue

                patching.apply_patch(id, wad)

                wad_data = cStringIO.StringIO()
                wad.writeto(wad_data)

                output_file.writestr(filename, wad_data.getvalue())

            except Exception:
                print('Error: Failed to add {0}'.format(filename))
                continue

        cached_file.close()

    add_lump(output_file, 'KEYCONF')
    add_lump(output_file, 'MENUDEF')

    output_file.close()

if __name__ == '__main__':
    main()
